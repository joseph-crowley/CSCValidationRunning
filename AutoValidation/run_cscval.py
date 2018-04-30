#! /usr/bin/env python

# CSC Validation submit script
#   Primary submission script for CSCValidation processing. Outputs are available
#   at http://cms-project-csc-validation.web.cern.ch/cms-project-csc-validation/
#
# Authors
#   Ben Knapp, Northeastern University
#   Devin Taylor, UW-Madison

######################################################
###############   Configuration   ####################
######################################################

import os
import sys
import fileinput
import string
import time
import subprocess
import argparse
import re
import errno
import math
from dbs.apis.dbsClient import DbsApi

# No run numbers below MINRUN will be processed
# This parameter is ignored if the "-rn" option is specified on the command line
MINRUN = 300576 # test

pipe = subprocess.PIPE
Release = subprocess.Popen('echo $CMSSW_VERSION', shell=True, stdout=pipe).communicate()[0]
Release = Release.rstrip("\n")

########## Directories #############

TEMPLATE_PATH = '%s/src/CSCValidationRunning/Templates' % os.environ['CMSSW_BASE']
RESULT_PATH = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/results'
WWW_PATH = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results'
CRAB_PATH = '/eos/cms/store/group/dpg_csc/comm_csc/cscval/crab_output'
BATCH_PATH = '/eos/cms/store/group/dpg_csc/comm_csc/cscval/batch_output'

####################################


#####################
##### Utilities #####
#####################
def fix_stream(dataset):
    _,stream,version,_ = dataset.split("/")
    return stream+version.replace("_","")

def python_mkdir(dir):
    '''A function to make a unix directory as well as subdirectories'''
    try:
        os.makedirs(dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else: raise

def replace(map, fileInName, fileOutName, moreLines=[]):
    '''Replace template file parameters'''
    replace_items = map.items()
    open(fileOutName,'w').close()
    with open(fileInName,'r') as filein:
        for line in filein:
            for old, new in replace_items:
                line = string.replace(line, old, new)
            with open(fileOutName,'a') as fileout:
                fileout.write(line)
    for line in moreLines:
        for old, new in replace_items:
            line = string.replace(line, old, new)
        with open(fileOutName,'a') as fileout:
            fileout.write(line)

################################
##### Validation functions #####
################################
def run_validation(dataset,globalTag,run,maxJobNum,stream,eventContent,num,input_files,**kwargs):
    '''
    The primary validation routine. Creates working directories and submits jobs to crab.
    '''
    force = kwargs.pop('force',False)
    triggers = kwargs.pop('triggers',[])
    dryRun = kwargs.pop('dryRun',False)
    runCrab = False

    # Create working directory for specific run number
    rundir = 'run_%s' % run
    python_mkdir(rundir)
    os.chdir(rundir)

    # Use appropriate cfg files in Templates directory for
    # first, running the validation to get CSC DQM & EMTF plots and
    # second, merging the resultant files to create plots, and push them to the EOS website
    if "GEN" in eventContent: eventContent = "RAW"
    paramMap = {
        'RECO' : {
            'digis': False,
            'standalone': True,
        },
        'FEVT' : {
            'digis': True,
            'standalone': True,
        },
        'RAW' : {
            'digis': True,
            'standalone': False,
        },
    }
    # TODO: eventually add options for custom configs
    if paramMap[eventContent]['digis']:
        cfg  = 'cfg_yesDigis_%s_template' % eventContent
        crab = 'crab_yesDigis_%s_template' % eventContent
        proc = 'secondStep_yesDigis_template'
        if eventContent=='FEVT' and 'HI' in dataset: cfg += '_HI'
    else:
        cfg  = 'cfg_noDigis_%s_template' % eventContent
        crab = 'crab_noDigis_%s_template' % eventContent
        proc = 'secondStep_noDigis_template'

    print "Will run with options --- \nDigis: %r \nStandalone: %r" % (paramMap[eventContent]['digis'], paramMap[eventContent]['standalone'])
    print "\nUsing the following cfg template files --- \ncfg: "+cfg+"\ncrab: "+crab+"\nproc: "+proc

    templatecfgFilePath = '%s/%s' %(TEMPLATE_PATH, cfg)
    templatecrabFilePath = '%s/%s' % (TEMPLATE_PATH, crab)
    templateHTMLFilePath = '%s/html_template' % TEMPLATE_PATH
    templateRootMacroPath = '%s/makePlots.C' % TEMPLATE_PATH
    templateGraphMacroPath = '%s/makeGraphs.C' % TEMPLATE_PATH
    templateRootMacroEMTFPath = '%s/makePlots_emtf.C' % TEMPLATE_PATH
    templateSecondStepPath = '%s/%s' % (TEMPLATE_PATH, proc)

    # old HTML stuff, kept for backwards compatibility
    cfgFileName='validation_%s_cfg.py' % run
    crabFileName='crab_%s_cfg.py' % run
    htmlFileName = "Summary.html"
    macroFileName = {}
    macroFileName['All'] = "makePlots.C"
    macroFileName['Graph'] = "makeGraphs.C"
    for trigger in triggers:
        macroFileName[trigger] = "%s_makePlots.C" % trigger
    macroFileNameEMTF = "makePlots_emtf.C"
    procFileName = "secondStep.py"
    outFilePrefix='valHists_run%s_%s' % (run, stream)
    outFileName='%s.root' % (outFilePrefix)
    outEMTFName='emtfHist_run%s_%s.root' % (run, stream)
    outputPath = '%s/%s/run%s_%s' % (BATCH_PATH, stream, run, eventContent)
    Time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

    symbol_map_html = { 'RUNNUMBER':run, 'NEVENT':num, "DATASET":dataset, "CMSSWVERSION":Release, "GLOBALTAG":globalTag, "DATE":Time }
    symbol_map_macro = {}
    symbol_map_macro['All'] = { 'FILENAME':outFileName, 'TEMPLATEDIR':TEMPLATE_PATH }
    symbol_map_macro['Graph'] = { 'INPUTDIR':outputPath, 'FILEPREFIX':outFilePrefix, 'TEMPLATEDIR':TEMPLATE_PATH }
    for trigger in triggers:
        symbol_map_macro[trigger] = { 'FILENAME':trigger+'_'+outFileName, 'TEMPLATEDIR':TEMPLATE_PATH }
    symbol_map_emtf = {'FILENAME': outEMTFName, 'TEMPLATEDIR':TEMPLATE_PATH, 'RUNNUMBER':run}
    symbol_map_proc = { 'TEMPLATEDIR':TEMPLATE_PATH, 'OUTPUTFILE':outFileName, 'RUNNUMBER':run, 'NEWDIR':rundir, 'CFGFILE':cfgFileName, 'STREAM':stream }
    symbol_map_cfg = { 'NEVENT':num, 'GLOBALTAG':globalTag, "OUTFILE":outFileName, 'DATASET':dataset, 'RUNNUMBER':run}
    symbol_map_crab = { 'GLOBALTAG':globalTag, "OUTFILE":outFileName, 'DATASET':dataset, 'RUNNUMBER':run, 'STREAM':stream, 'EVENTCONTENT':eventContent}

    trigger_cfg = []
    trigger_proc = []
    for trigger in triggers:
        trigger_cfg += ["process.triggerSelection%s = process.triggerSelection.clone(triggerConditions=cms.vstring('%s'))\n" %(trigger, trigger)]
        trigger_cfg += ["process.cscValidation%s = process.cscValidation.clone(rootFileName=cms.untracked.string('%s_OUTFILE'))\n" % (trigger, trigger)]
        trigger_cfg += ["process.p%s = cms.Path(process.gtDigis * process.triggerSelection%s * process.muonCSCDigis * process.csc2DRecHits * process.cscSegments * process.cscValidation%s)\n" % (trigger, trigger, trigger)]
        trigger_proc += ["print '%s'\n" % trigger]
        trigger_proc += ['os.system("root -l -q -b %s_makePlots.C")\n' % trigger]
        trigger_proc += ['os.system("mkdir -p /eos/cms/store/group/dpg_csc/comm_csc/cscval/www/results/runRUNNUMBER/STREAM/Site/PNGS/%s")\n' % trigger ]
        trigger_proc += ['os.system("cp *.png /eos/cms/store/group/dpg_csc/comm_csc/cscval/www/results/runRUNNUMBER/STREAM/Site/PNGS/%s")\n' % trigger ]
        trigger_proc += ['os.system("mkdir -p /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/results/runRUNNUMBER/STREAM/Site/PNGS/%s")\n' % trigger ]
        trigger_proc += ['os.system("mv *.png /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/results/runRUNNUMBER/STREAM/Site/PNGS/%s")\n' % trigger ]


    replace(symbol_map_html,templateHTMLFilePath, htmlFileName)
    replace(symbol_map_macro['All'],templateRootMacroPath, macroFileName['All'])
    replace(symbol_map_macro['Graph'],templateGraphMacroPath, macroFileName['Graph'])
    for trigger in triggers:
        replace(symbol_map_macro[trigger],templateRootMacroPath, macroFileName[trigger])
    replace(symbol_map_emtf,templateRootMacroEMTFPath, macroFileNameEMTF)
    replace(symbol_map_proc,templateSecondStepPath, procFileName, trigger_proc)
    replace(symbol_map_cfg,templatecfgFilePath, cfgFileName, trigger_cfg)
    replace(symbol_map_crab,templatecrabFilePath, crabFileName)

    os.system("chmod 755 secondStep.py")

    jsonStr = 'var runParams = {\n' \
            + '  "release" : "%s",\n' % Release \
            + '  "datasetname" : "%s",\n' % dataset \
            + '  "runnum" : "%s",\n' % run \
            + '  "events" : "%s",\n' % num \
            + '  "globaltag" : "%s",\n' % globalTag \
            + '  "rundate" : "%s",\n' % Time \
            + '  "triggers" : [\n' \
            + '    "All"'
    for trigger in triggers:
        jsonStr += ',\n    "%s"' % trigger
    jsonStr += '\n  ]\n}'

    with open('runParams.json','w') as file:
        file.write(jsonStr)

    # After renaming, etc. all of the appropriate cfg files, create the corresponding
    # submission script (either for CRAB or lxbatch) and submit
    if runCrab:
        # If runCrab then do a crab submit for the crab cfg file
        sh = open("run.sh", "w")
        sh.write("#!/bin/bash \n")
        sh.write("aklog \n")
        sh.write('source /afs/cern.ch/cms/cmsset_default.sh \n')
        rundir = subprocess.Popen("pwd", shell=True,stdout=pipe).communicate()[0]
        rundir = rundir.rstrip("\n")
        sh.write("cd "+rundir+" \n")
        sh.write("eval `scramv1 runtime -sh` \n")
        sh.write("cd - \n")
        RUN_BASH = "crab submit -c "+crabFileName
        sh.write(RUN_BASH+" \n")
        sh.close()

        # submit to crab
        print "Submitting to crab"
        subprocess.check_call("bash run.sh", shell=True)

    else:
        #If runCrab is false, then need to create output directory on EOS,
        #decide how many batch jobs to submit (depends on number of input files),
        #modify the the cfg file template name for every individual file submitted,
        #build a submission script for each of these input files that runs the Validation
        #and copies the output rootfiles (for CSC DQM and EMTF) to the EOS folder,
        #and then finally submits the job
        subprocess.check_call('mkdir -p /eos/cms/store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s' % (stream, run, eventContent), shell=True)
        nf = 1
        # maxJobNum controls the maximum number of jobs to submit if numJobs is very large
        #maxJobNum = 2
        print "\nMaximum number of batch jobs submitted per run: "+str(maxJobNum)+"\n"
        # numJobs is the parameter to decide how many batch jobs to submit for the total number of input files for a run
        numJobs = int(math.ceil(len(input_files)/float(nf)))
        # check files already run over
        fname = 'processedFiles.txt'
        open(fname, 'a').close()
        with open(fname, 'r') as file:
            procFiles = file.readlines()
        procFiles = [x.rstrip() for x in procFiles]
         
        for j in range(min(maxJobNum, numJobs)):
            doJob = force
            for f in input_files[j*nf:j*nf+nf]:
                if f not in procFiles:
                    doJob = True
                    if not dryRun:
                        with open(fname, 'a') as file:
                            file.write('%s\n'%f)

            if not doJob: continue

            # rename the file to unique
            fn = input_files[j*nf].split('/')[-1].split('.')[0]
            cfgFileName='validation_%s_%s_cfg.py' % (run, fn)
            outFileName='valHists_run%s_%s_%s.root' % (run, stream, fn)
            inEMTFName='DQM_V0001_YourSubsystem_R000%s.root' % run
            outEMTFName='emtfHist_run%s_%s_%s.root' % (run, stream, fn)

            # create the config file
            fileListString = ''
            numLumis = 0
            numEvents = 0
            for f in input_files[j*nf:j*nf+nf]:
                if fileListString: fileListString += ',\n'
                fileListString += "    '%s'" % f

            symbol_map_cfg = { 'NEVENT':num, 'GLOBALTAG':globalTag, "OUTFILE":outFileName, 'DATASET':dataset, 'RUNNUMBER':run, 'FILELIST': fileListString, 'VERSION': str(j)}
            replace(symbol_map_cfg,templatecfgFilePath, cfgFileName, trigger_cfg)

            # create a submission script
            sh = open("run_%i.sh" % j, "w")
            sh.write("#!/bin/bash \n")
            sh.write("aklog \n")
            sh.write('source /afs/cern.ch/cms/cmsset_default.sh \n')
            rundir = subprocess.Popen("pwd", shell=True,stdout=pipe).communicate()[0]
            rundir = rundir.rstrip("\n")
            sh.write("cd "+rundir+" \n")
            sh.write("eval `scramv1 runtime -sh` \n")
            sh.write("cd - \n")
            sh.write('cmsRun %s/%s\n' % (rundir, cfgFileName))
            sh.write('cp %s /eos/cms/store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (outFileName, stream, run, eventContent, outFileName))
            for trigger in triggers:
                sh.write('cp %s_%s /eos/cms/store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s_%s\n' % (trigger, outFileName, stream, run, eventContent, trigger, outFileName))
            sh.write('cp %s /eos/cms/store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (inEMTFName, stream, run, eventContent, outEMTFName))
            sh.write('cp TPEHists_%i.root /eos/cms/store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/TPEHists_%i.root\n' % (j, stream, run, eventContent, j))
            # sh.write('chmod g+w /eos/cms/store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/\n' % (stream, run, eventContent))
            sh.close()

            print "Submitting job %i out of %i total files" % (j+1, numJobs)
            #queue = '1nh' if 'Express' in stream else '8nh'
            queue = '8nh'
            if not dryRun: subprocess.check_call("LSB_JOB_REPORT_MAIL=N bsub -q %s -J %s_%s_%i < run_%i.sh" % (queue, run, stream, j, j), shell=True)

    os.chdir('../')

    return 0

def process_output(dataset,globalTag,**kwargs):
    '''
    Script to retrieve the output from EOS, merge the histograms, and create the images.
    '''
    # Grab arguments specified as flags on the command line
    force = kwargs.pop('force',False)
    runN = kwargs.pop('run',0)
    maxJobNum = kwargs.get('maxjobs', 200)
    triggers = kwargs.pop('triggers',[])
    dryRun = kwargs.pop('dryRun',False)
    [filler, stream, version, eventContent] = dataset.split('/')
    if "GEN" in dataset: stream = fix_stream(dataset)
    os.chdir(stream)
  
    if not maxJobNum:
        maxJobNum = 200

    runCrab = False

    runsToPlot = []

    if force: print 'Forcing remerging'
    # get available runs in eos
    for job in subprocess.Popen('ls %s/%s' % (CRAB_PATH if runCrab else BATCH_PATH,stream), shell=True,stdout=pipe).communicate()[0].splitlines():
        # go to working area
        if runCrab:
            [type, runStr, runEventContent] = job.split('_')
        else:
            [runStr,runEventContent] = job.split('_')
        run = runStr[3:]
        # runN is the run number if option "-rn" is specified
        if runN:
            if str(runN) != run: continue
        else:
            if int(run)<MINRUN: continue

        # some job still running. skip.
        #if "Job <%s_%s*> is not found" % (run,stream) not in subprocess.Popen("unbuffer bjobs -J %s_%s*" % (run,stream), shell=True,stdout=pipe).communicate()[0].splitlines():
        #    print 'Run %s %s not finished' % (run,stream)
        #    continue
        # dont rerun if current merge
        if "Job <%s_%smerge> is not found" % (run,stream) not in subprocess.Popen("unbuffer bjobs -J %s_%smerge" % (run,stream), shell=True,stdout=pipe).communicate()[0].splitlines():
            print 'Run %s %s not finished' % (run,stream)
            continue

        rundir = 'run_%s' % run
        python_mkdir(rundir)
        os.chdir(rundir)

        tpeOut = 'TPEHists.root'
        valOut = {}
        valOut['All'] = 'valHists_run%s_%s.root' % (run, stream)
        emtfOut = 'emtfHist_run%s_%s.root' % (run, stream)
        for trigger in triggers:
            valOut[trigger] = '%s_valHists_run%s_%s.root' % (trigger, run, stream)

        if runCrab:
            # get last job (in case we reprocessed)
            jobVersion = ''
            for jv in subprocess.Popen('eos ls %s/%s/%s' % (CRAB_PATH,stream,job), shell=True,stdout=pipe).communicate()[0].splitlines():
                jobVersion = jv
            fileDir = '%s/%s/%s/%s/0000' % (CRAB_PATH,stream,job,jobVersion)
        else:
            jobVersion = 'job'
            fileDir = '%s/%s/%s' % (BATCH_PATH,stream,job)
        tpeFiles = []
        valFiles = {}
        valFiles['All'] = []
        emtfFiles = []
        for trigger in triggers:
            valFiles[trigger] = []

        # clean fileDir for files under 512 first, but skip TPEHists
        subprocess.check_call("find %s -name \"*run*.root\" -size -1b -delete" % fileDir, shell=True)
        for file in subprocess.Popen('eos ls %s' % (fileDir), shell=True,stdout=pipe).communicate()[0].splitlines():
            if file==tpeOut or file==valOut['All'] or file==emtfOut: continue
            if file[0:3]=='TPE': tpeFiles += [file]
            if file[0:3]=='val': valFiles['All'] += [file]
            for trigger in triggers:
                if file.startswith('%s_val' % trigger): valFiles[trigger] += [file]
            if file[0:4]=='emtf': emtfFiles += [file]
        nFiles = len(valFiles['All'])
        if len(tpeFiles) == 0 or float(nFiles)/len(tpeFiles) < 0.7:
            print "Less than 7/10 of Validation root files out of the total number of batch jobs got through"
	    print "May need to re-do the validation for run #%s..." % run 

        # see if we need to remerge things
        processedString = '%s_%i' %(jobVersion, nFiles)
        fname = 'out.txt'
        open(fname, 'a').close()
        with open(fname,'r') as file:
            oldProcessedString = file.readline().rstrip()

        if not force:
            if oldProcessedString == processedString:
                os.chdir('../')
                continue

        print "Processing %s run %s" % (stream, run)

        with open(fname,'w') as file:
            file.write(processedString)

        # and merge them
        #nFiles is the total number of validation CSC DQM ROOT files
        maxJobSize = 400
        nMerges = nFiles / maxJobSize + 1
        for imerge in range(0, nMerges):
            if imerge > 1: continue      # effectively set maximum files to 2*maxJobSize
            # prepare remerge string
            remergeString =  '[[ ! $? ]] && echo "Merge failed, try remerging"\n'
            remergeString += 'failstr=$(grep "hadd exiting" mergeout_%s.txt)\n' % imerge
            remergeString += 'while [[ $failstr ]]; do\n'
            remergeString += '    badfile=$(echo $failstr | cut -c30-)\n'
            remergeString += '    echo "Removing bad file $badfile" >&2\n'
            remergeString += '    rm $badfile\n'
            remergeString += '    $valfiles=${valfile/$badfile/}\n'
            remergeString += '    mv mergeout_{}.txt $baseDir/mergeout_$(date +"%H%M%S").txt\n'.format(imerge)
            remergeString += '    hadd -T -k -n 100 -f $target $valfiles > mergeout_%s.txt 2>&1\n' % imerge
            remergeString += '    failstr=$(grep "hadd exiting" mergeout_%s.txt)\n' % imerge
            remergeString += 'done\n'
            # remergeString += 'failstr=$(grep "error reading all" mergeout_%s.txt)\n' % imerge
            remergeString += 'failstr=$(grep "error" mergeout_%s.txt)\n' % imerge
            remergeString += '[[ ! -z $failstr ]] && mv mergeout_{}.txt $baseDir/mergefailed_$(date +"%H%M%S").txt\n'.format(imerge)

            mergeScriptStr  = "#!/bin/bash \n"
            mergeScriptStr += "aklog \n"
            mergeScriptStr += 'source /afs/cern.ch/cms/cmsset_default.sh \n'
            rundir = subprocess.Popen("pwd", shell=True,stdout=pipe).communicate()[0]
            rundir = rundir.rstrip("\n")
            mergeScriptStr += "cd "+rundir+" \n"
            mergeScriptStr += "eval `scramv1 runtime -sh` \n"
            mergeScriptStr += "cd - \n"
            mergeScriptStr += "baseDir=%s\n" % rundir
            mergeScriptStr += "cd %s\n" % fileDir

            sh = open("merge_val_%s.sh" % imerge, "w")
            sh.write(mergeScriptStr)
            if valFiles['All']:
                print "\nMerging valHists"
                sh.write("cd %s\n" % fileDir)
                valfiles = valFiles['All'][imerge*maxJobSize : (imerge+1)*maxJobSize]
                valMergeString  = 'target=merge_valHists_%s.root\n' % imerge
                valMergeString += 'valfiles="'
                for val in valfiles:
                    valMergeString += ' %s' % val
                valMergeString += '"\n'
                valMergeString += 'hadd -T -k -j 4 -f $target $valfiles > mergeout_%s.txt 2>&1\n' % imerge
                # valMergeString += 'root -l -b -q replaceTreeWithGraphs.C"(\\"$target\\")" >> mergeout_%s.txt\n' % imerge
                sh.write(valMergeString+'\n')
                sh.write(remergeString)
                sh.write('mv mergeout_{}.txt $baseDir/mergeout_$(date +"%H%M%S").txt\n'.format(imerge))

            sh.write('cp merge_valHists_%s.root $baseDir\n' % imerge)
            sh.write('cd %s\n' % rundir)
            sh.close()
            if not dryRun: subprocess.check_call("LSB_JOB_REPORT_MAIL=N bsub -R \"pool>3000\" -q 8nh -J %s_%smerge_%s < merge_val_%s.sh" % (run,stream,imerge,imerge), shell=True)

            sh = open("merge_emtf_%s.sh" % imerge, "w")
            sh.write(mergeScriptStr)
            if emtfFiles:
                print "Merging emtfHists"
                sh.write("cd %s\n" % fileDir)
                emtffiles = emtfFiles[imerge*maxJobSize : (imerge+1)*maxJobSize]
                emtfMergeString  = 'target=merge_emtfHist_%s.root\n' % imerge
                emtfMergeString += 'valfiles="'
                for emtf in emtffiles:
                    emtfMergeString += ' %s' % emtf
                emtfMergeString += '"\n'
                emtfMergeString += 'hadd -T -k -j 4 -f $target $valfiles > mergeout_emtf_%s.txt 2>&1\n' % imerge
                sh.write(emtfMergeString+'\n')
                # sh.write(remergeString)
                sh.write('mv mergeout_emtf_{}.txt $baseDir/mergeout_emtf_$(date +"%H%M%S").txt\n'.format(imerge))

            sh.write('cp merge_emtfHist_%s.root $baseDir\n' % imerge)
            sh.write('cd %s\n' % rundir)
            sh.close()
            if not dryRun: subprocess.check_call("LSB_JOB_REPORT_MAIL=N bsub -R \"pool>3000\" -q 8nh -J %s_%smerge_emtf_%s < merge_emtf_%s.sh" % (run,stream,imerge,imerge), shell=True)

        runsToPlot += [[run,job,nMerges]]

        os.chdir('../')

    updateRunlist = len(runsToPlot)
    # now plot the merges as they finish
    remainingJobs = runsToPlot
    while remainingJobs:
        runsToPlot = remainingJobs
        remainingJobs = []
        for run,job,nMerges in runsToPlot:
            # go to working area
            rundir = 'run_%s' % run
            python_mkdir(rundir)
            os.chdir(rundir)

            tpeOut = 'TPEHists.root'
            valOut = {}
            valOut['All'] = 'valHists_run%s_%s.root' % (run, stream)
            for trigger in triggers:
                valOut[trigger] = '%s_valHists_run%s_%s.root' % (trigger, run, stream)
            emtfOut = 'emtfHist_run%s_%s.root' % (run, stream)

            # wait for job to finish then copy over
            print("Waiting on run %s" % run)
            runningMergeJobs = subprocess.Popen("bjobs -w | grep %s_%smerge" % (run,stream), shell=True,stdout=pipe).communicate()[0].splitlines()
            if runningMergeJobs:
                time.sleep(20)
                remainingJobs += [[run,job,nMerges]]
            else:
                if dryRun: continue
                print("Run %s merged" % run)
                valRet = subprocess.call('hadd -k -f %s `ls merge_valHists_*.root` ' % (valOut['All']), shell=True)
                subprocess.call('hadd -k -f %s `ls merge_emtfHist_*.root` ' % (emtfOut), shell=True)
                # valRet = subprocess.call('mv merge_valHists_0.root %s' % (valOut['All']), shell=True) # temporary
                # subprocess.call('mv merge_emtfHist_0.root %s' % (emtfOut), shell=True) # temporary
                if valRet: valRet = subprocess.call('mv merge_valHists_0.root %s' % (valOut['All']), shell=True) # temporary
                if not valRet: os.system("./secondStep.py")
                #andrew -- comment out next line to keep merged rootfiles in work directory as well
                #subprocess.call('rm *.root', shell=True)

            os.chdir('../')

    os.chdir('../')

    if updateRunlist and not force:
        build_runlist()

    return 0

def build_runlist():
    Time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    tstamp = time.strftime("%H%M%S", time.localtime())
    print >> sys.stderr, "[%s] Building runlist for afs" % Time
    os.system('bash generateRunList.sh /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/results > temp_afs_runlist_%s.json' % tstamp)
    os.system('mv temp_afs_runlist_%s.json /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/js/runlist.json' % tstamp)
    print >> sys.stderr, "[%s] Building runlist for eos" % Time
    os.system('bash generateRunList.sh > temp_eos_runlist_%s.json' % tstamp)
    os.system('cat temp_eos_runlist_%s.json > /eos/cms/store/group/dpg_csc/comm_csc/cscval/www/js/runlist.json' % tstamp)
    os.system('rm temp_eos_runlist_%s.json' % tstamp)
    # create last run json
    with open('lastrun.json','w') as file:
        file.write('var lastrun = {\n  "lastrun" : "%s"\n}\n' % Time)
    os.system('cat lastrun.json > /eos/cms/store/group/dpg_csc/comm_csc/cscval/www/js/lastrun.json')
    os.system('mv lastrun.json /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/js/')
    return 0


def process_dataset(dataset,globalTag,**kwargs):
    '''
    Script to call validation of multiple runs
      kwargs:
        argument    type      default    comment
        run         int       0          if nonzero, will process a single run, else, process all available
        force       bool      False      do a run regardless if processed already or number of events
        triggers    list(str) []         list of additional triggers to run over
    '''
    singleRun = kwargs.pop('run',0)
    force = kwargs.pop('force',False)
    dryRun = kwargs.get('dryRun',False)
    maxJobNum = kwargs.get('maxjobs', 200)
    curTime = time.time()

    if not maxJobNum:
        maxJobNum = 200

    url = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader'
    dbsclient = DbsApi(url)

    # get stream info
    [filler, stream, version, eventContent] = dataset.split('/')
    if "GEN" in dataset: stream = fix_stream(dataset)

    # setup working directory for stream
    python_mkdir(stream)

    # begin running
    start=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    print "CSCVal job initiated at "+start
    os.chdir(stream)

    print "Reading previously processed runs"
    procFile = 'processedRuns.txt'
    open(procFile, 'a').close()
    with open(procFile, 'r') as file:
        procRuns = file.readlines()
    procRuns = [x.rstrip() for x in procRuns] # format: RUNUM_NUMEVTS

    print "Reading previous process time"
    timeFile = 'processTime.txt'
    open(timeFile, 'a').close()
    with open(timeFile, 'r') as file:
        procTimes = file.readlines()
    procTimes = [x.rstrip() for x in procTimes]
    prevTime = float(procTimes[-1]) - 12*60*60 if procTimes else float(time.time()) - 7*24*60*60 # default to 7 days before now or 12 hours before last run
    print "prevTime = "+str(prevTime)

    # run each individual validation
    if singleRun:
        files = dbsclient.listFiles(dataset=dataset, run_num=singleRun, validFileOnly=1, detail=True)
        num = sum([f['event_count'] for f in files])
        print "\nNumber of events in all files listed in DAS for this run/dataset: "+str(num)
        input_files = [f['logical_file_name'] for f in files]

        #print "--> Printing the LFN of all input files for run #%s:" % str(singleRun)
        #print input_files

        print "Processing run %s" % str(singleRun)
        if force: print "Forcing reprocessing"
        run_validation(dataset, globalTag, str(singleRun), maxJobNum, stream, eventContent, str(num), input_files, force=force, **kwargs)
    else:
        # first get new blocks since a time
        blocks = dbsclient.listBlocks(dataset=dataset, min_cdate=int(prevTime))

        # iterate over each block
        updatedRuns = set()
        for block in blocks:
            # get runs in block
            runs = dbsclient.listRuns(block_name=block['block_name'])
            updatedRuns.update(set(runs[0]['run_num']))

        # iterate over runs
        updatedRuns = sorted(updatedRuns)
        fileRunMap = {}
        eventRunMap = {}
        files = dbsclient.listFiles(dataset=dataset, run_num=updatedRuns, validFileOnly=1, detail=True)
        if "GEN" in dataset: updatedRuns = [1]
        for run in updatedRuns:
            eventRunMap[run] = sum([f['event_count'] for f in files if f['run_num']==run])
            fileRunMap[run] = [f['logical_file_name'] for f in files if f['run_num']==run]


        runsToUpdate = [run for run in updatedRuns if fileRunMap[run] and eventRunMap[run]>25000]
        if "GEN" in dataset: runsToUpdate = [run for run in updatedRuns if fileRunMap[run]]

        print 'Runs to update:'
        for run in runsToUpdate:
            print '    Run {0}: {1} files, {2} events'.format(run,len(fileRunMap[run]),eventRunMap[run])

        for run in runsToUpdate:
            if int(run)<MINRUN: continue
            print "Processing run %s" % run
            run_validation(dataset, globalTag, str(run), maxJobNum, stream, eventContent, str(eventRunMap[run]), fileRunMap[run], force=force, **kwargs)

    with open(timeFile, 'a') as file:
        if not dryRun: file.write('{0}\n'.format(curTime))
    os.chdir('../')

    # now finish up
    end=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    print "CSCVal job finished at "+end


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description="Run CSCValidation")


    parser.add_argument('dataset', type=str, help='Select dataset (defines stream and event content)')
    parser.add_argument('globalTag', type=str, help='Define GlobalTag')
    parser.add_argument('-rn', '--runNumber', type=int, default=0, help='Process a specific run (defaults to all runs).')
    parser.add_argument('-ro', '--retrieveOutput', action='store_true',help='Retrieve the output of a previous run and produce the HTML.')
    #parser.add_argument('-rh', '--reprocessHistograms', action='store_true',help='Reprocess histograms (in case of changes to template, rather than CSCValidation.cc).')
    parser.add_argument('-br', '--buildRunlist', action='store_true',help='Build the runlist.json file for the website.')
    parser.add_argument('-dr', '--dryRun', action='store_true',help='Don\'t submit, just create the objects')
    parser.add_argument('-f','--force', action='store_true', help='Force a recipe (even if already processed).')
    parser.add_argument('-t','--triggers', nargs='*', help='Optionally run on additional triggers.')
    parser.add_argument('-mj','--maxJobNum', type=int, default=200, help='Can use to control the total number of batch jobs submitted out of all of the different files for a run (specified by LFN), as seen on DAS.')

    args = parser.parse_args(argv)
    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_command_line(argv)

    if not args.triggers: args.triggers = []

    ds = args.dataset.split('/')
    if len(ds) != 4:
        print 'Invalid dataset. Argument should be in the form of a DAS query (/*/*/*).'
        return 0

    if args.buildRunlist:
        build_runlist()
        return 0

    if args.retrieveOutput:
        #process_output, done by checking the '-ro' option, is the "second step" in the validation routine
        #responsible for merging all of the different output files from the first step,
        #making PNGS for each of the different plots from these files,
        #moving the PNGS to the www directory on EOS so they can be seen on the website,
        #and then building the run list at the end using the function build_runlist
        process_output(args.dataset, args.globalTag, force=args.force, run=args.runNumber, maxjobs=args.maxJobNum, triggers=args.triggers, dryRun=args.dryRun)
        return 0

    #if args.reprocessHistograms:
    #    return 0

    #process_dataset is the "first step" in the validation that pulls files using the Dbs client tool,
    #creates all of the needed config files and ROOT scripts (using the templates in the Templates folder)
    #and submits batch jobs (or CRAB jobs if runCrab) to run the Validation, yielding CSC DQM and EMTF files,
    #and finally moves these output ROOT files to the batch_output folder on EOS
    #Note: the function run_validation is utilized inside process_dataset
    process_dataset(args.dataset, args.globalTag, force=args.force, run=args.runNumber, maxjobs=args.maxJobNum, triggers=args.triggers, dryRun=args.dryRun)

    return 0

if __name__ == "__main__":
    main()
