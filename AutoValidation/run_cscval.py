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
from das_client import get_data, DASOptionParser

MINRUN = 265312 # Commissioning2016 MWGR2

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
def run_validation(dataset,globalTag,run,stream,eventContent,**kwargs):
    '''
    The primary validation routine. Creates working directories and submits jobs to crab.
    '''
    force = kwargs.pop('force',False)
    triggers = kwargs.pop('triggers',[])
    dryRun = kwargs.pop('dryRun',False)
    runCrab = False
    # create run working directory
    rundir = 'run_%s' % run
    python_mkdir(rundir)
    os.chdir(rundir)
    os.system("cp ../das_client.py .")
    
    # open appropriate config and crab submit files
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

    print "Will run with options: digis: %r standalone: %r" % (paramMap[eventContent]['digis'], paramMap[eventContent]['standalone'])

    templatecfgFilePath = '%s/%s' %(TEMPLATE_PATH, cfg)
    templatecrabFilePath = '%s/%s' % (TEMPLATE_PATH, crab)
    templateHTMLFilePath = '%s/html_template' % TEMPLATE_PATH
    templateRootMacroPath = '%s/makePlots.C' % TEMPLATE_PATH
    templateRootMacroCSCTFPath = '%s/makePlots_csctf.C' % TEMPLATE_PATH
    templateSecondStepPath = '%s/%s' % (TEMPLATE_PATH, proc)

    # get number of events in run
    num = subprocess.Popen("./das_client.py --limit=0 --query='summary dataset=%s run=%s | grep summary.nevents'" % (dataset,run), shell=True,stdout=pipe).communicate()[0].rstrip()
    nfiles = subprocess.Popen("./das_client.py --limit=0 --query='summary dataset=%s run=%s | grep summary.nfiles'" % (dataset,run), shell=True,stdout=pipe).communicate()[0].rstrip()
    nlumis = subprocess.Popen("./das_client.py --limit=0 --query='summary dataset=%s run=%s | grep summary.nlumis'" % (dataset,run), shell=True,stdout=pipe).communicate()[0].rstrip()

    print "Processing %s files, %s lumis, and %s events" % (nfiles, nlumis, num)

    # old HTML stuff, kept for backwards compatibility
    cfgFileName='validation_%s_cfg.py' % run
    crabFileName='crab_%s_cfg.py' % run
    htmlFileName = "Summary.html"
    macroFileName = {}
    macroFileName['All'] = "makePlots.C"
    for trigger in triggers:
        macroFileName[trigger] = "%s_makePlots.C" % trigger
    macroFileNameCSCTF = "makePlots_csctf.C"
    procFileName = "secondStep.py"
    outFileName='valHists_run%s_%s.root' % (run, stream)
    outCSCTFName='csctfHist_run%s_%s.root' % (run, stream)
    Time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

    symbol_map_html = { 'RUNNUMBER':run, 'NEVENT':num, "DATASET":dataset, "CMSSWVERSION":Release, "GLOBALTAG":globalTag, "DATE":Time }
    symbol_map_macro = {}
    symbol_map_macro['All'] = { 'FILENAME':outFileName, 'TEMPLATEDIR':TEMPLATE_PATH }
    for trigger in triggers:
        symbol_map_macro[trigger] = { 'FILENAME':trigger+'_'+outFileName, 'TEMPLATEDIR':TEMPLATE_PATH }
    symbol_map_csctf = {'FILENAME': outCSCTFName, 'TEMPLATEDIR':TEMPLATE_PATH, 'RUNNUMBER':run}
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
        trigger_proc += ['os.system("mkdir -p /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/results/runRUNNUMBER/STREAM/Site/PNGS/%s")\n' % trigger ]
        trigger_proc += ['os.system("mv *.png /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/results/runRUNNUMBER/STREAM/Site/PNGS/%s")\n' % trigger ]


    replace(symbol_map_html,templateHTMLFilePath, htmlFileName)
    replace(symbol_map_macro['All'],templateRootMacroPath, macroFileName['All'])
    for trigger in triggers:
        replace(symbol_map_macro[trigger],templateRootMacroPath, macroFileName[trigger])
    replace(symbol_map_csctf,templateRootMacroCSCTFPath, macroFileNameCSCTF)
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

    if runCrab:
        # create a submission script
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
        subprocess.check_call('cmsMkdir /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s' % (stream, run, eventContent), shell=True)
        input_files = []
        for n in subprocess.Popen("./das_client.py --query='file dataset="+dataset+" run="+run+" | grep file.name' --limit=0", shell=True,stdout=pipe).communicate()[0].splitlines():
                #s = 'root://cms-xrd-global.cern.ch/'+n
                input_files.append(n)
        nf = 1
        numJobs = int(math.ceil(len(input_files)/float(nf)))
        for j in range(numJobs):
            # check files already run over
            fname = 'processedFiles.txt'
            open(fname, 'a').close()
            with open(fname, 'r') as file:
                procFiles = file.readlines()
            procFiles = [x.rstrip() for x in procFiles]

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
            inCSCTFName='DQM_V0001_YourSubsystem_R000%s.root' % run
            outCSCTFName='csctfHist_run%s_%s_%s.root' % (run, stream, fn)

            # create the config file
            fileListString = ''
            numLumis = 0
            numEvents = 0
            for f in input_files[j*nf:j*nf+nf]:
                if fileListString: fileListString += ',\n'
                fileListString += "    %s" % f

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
            sh.write('cmsStage -f %s /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (outFileName, stream, run, eventContent, outFileName))
            for trigger in triggers:
                sh.write('cmsStage -f %s_%s /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s_%s\n' % (trigger, outFileName, stream, run, eventContent, trigger, outFileName))
            sh.write('cmsStage -f %s /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (inCSCTFName, stream, run, eventContent, outCSCTFName))
            sh.write('cmsStage -f TPEHists_%i.root /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/TPEHists_%i.root\n' % (j, stream, run, eventContent, j))
            sh.close()

            print "Submitting job %i of %i" % (j+1, numJobs)
            #queue = '1nh' if 'Express' in stream else '8nh'
            queue = '8nh'
            if not dryRun: subprocess.check_call("LSB_JOB_REPORT_MAIL=N bsub -q %s -J %s_%s_%i < run_%i.sh" % (queue, run, stream, j, j), shell=True)

    os.chdir('../')

    return 0

def process_output(dataset,globalTag,**kwargs):
    '''
    Script to retrieve the output from EOS, merge the histograms, and create the images.
    '''
    force = kwargs.pop('force',False)
    runN = kwargs.pop('run',0)
    triggers = kwargs.pop('triggers',[])
    dryRun = kwargs.pop('dryRun',False)
    [filler, stream, version, eventContent] = dataset.split('/')
    os.chdir(stream)

    runCrab = False

    runsToPlot = []

    if force: print 'Forcing remerging'
    # get available runs in eos
    for job in subprocess.Popen('/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls %s/%s' % (CRAB_PATH if runCrab else BATCH_PATH,stream), shell=True,stdout=pipe).communicate()[0].splitlines():
        # go to working area
        if runCrab:
            [type, runStr, runEventContent] = job.split('_')
        else: 
            [runStr,runEventContent] = job.split('_')
        run = runStr[3:]
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
        csctfOut = 'csctfHist_run%s_%s.root' % (run, stream)
        for trigger in triggers:
            valOut[trigger] = '%s_valHists_run%s_%s.root' % (trigger, run, stream)

        if runCrab:
            # get last job (in case we reprocessed)
            jobVersion = ''
            for jv in subprocess.Popen('/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls %s/%s/%s' % (CRAB_PATH,stream,job), shell=True,stdout=pipe).communicate()[0].splitlines():
                jobVersion = jv
            fileDir = '%s/%s/%s/%s/0000' % (CRAB_PATH,stream,job,jobVersion)
        else:
            jobVersion = 'job'
            fileDir = '%s/%s/%s' % (BATCH_PATH,stream,job)
        tpeFiles = []
        valFiles = {}
        valFiles['All'] = []
        csctfFiles = []
        for trigger in triggers:
            valFiles[trigger] = []
        for file in subprocess.Popen('/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls %s' % (fileDir), shell=True,stdout=pipe).communicate()[0].splitlines():
            if file==tpeOut or file==valOut or file==csctfOut: continue
            if file[0:3]=='TPE': tpeFiles += [file]
            if file[0:3]=='val': valFiles['All'] += [file]
            for trigger in triggers:
                if file.startswith('%s_val' % trigger): valFiles[trigger] += [file]
            if file[0:5]=='csctf': csctfFiles += [file]
        nFiles = len(valFiles['All'])

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
        sh = open("merge.sh", "w")
        sh.write("#!/bin/bash \n")
        sh.write("aklog \n")
        sh.write('source /afs/cern.ch/cms/cmsset_default.sh \n')
        rundir = subprocess.Popen("pwd", shell=True,stdout=pipe).communicate()[0]
        rundir = rundir.rstrip("\n")
        sh.write("cd "+rundir+" \n")
        sh.write("eval `scramv1 runtime -sh` \n")
        sh.write("cd - \n")
        if tpeFiles:
            print "Merging tpeHists"
            tpeMergeString = 'hadd -f %s' % tpeOut
            for tpe in tpeFiles:
                tpeMergeString += ' root://eoscms.cern.ch/%s/%s' % (fileDir, tpe)
            sh.write(tpeMergeString+" \n")
            sh.write('cmsStage -f %s /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (tpeOut, stream, run, eventContent, tpeOut))
        if valFiles['All']:
            print "Merging valHists"
            valMergeString = 'hadd -f %s' % valOut['All']
            for val in valFiles['All']:
                if val==valOut['All']: continue # skip previous merge
                valMergeString += ' root://eoscms.cern.ch/%s/%s' % (fileDir, val)
            sh.write(valMergeString+" \n")
            sh.write('cmsStage -f %s /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (valOut['All'], stream, run, eventContent, valOut['All']))
        for trigger in triggers:
            if valFiles[trigger]:
                print "Merging %s_valHists" % trigger
                valMergeString = 'hadd -f %s' % valOut[trigger]
                for val in valFiles[trigger]:
                if val==valOut[trigger]: continue # skip previous merge
                    valMergeString += ' root://eoscms.cern.ch/%s/%s' % (fileDir, val)
                sh.write(valMergeString+" \n")
                sh.write('cmsStage -f %s /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (valOut[trigger], stream, run, eventContent, valOut[trigger]))
        if csctfFiles:
            print "Merging csctfHists"
            csctfMergeString = 'hadd -f %s' % csctfOut
            for csctf in csctfFiles:
                if csctf==csctfOut: continue # skip previous merge
                csctfMergeString += ' root://eoscms.cern.ch/%s/%s' % (fileDir, csctf)
            sh.write(csctfMergeString+" \n")
            sh.write('cmsStage -f %s /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (csctfOut, stream, run, eventContent, csctfOut))
        sh.close()
        if not dryRun: subprocess.check_call("LSB_JOB_REPORT_MAIL=N bsub -q 8nh -J %s_%smerge < merge.sh" % (run,stream), shell=True)

        runsToPlot += [[run,job]]

        os.chdir('../')

    # now plot the merges as they finish
    for run,job in runsToPlot:
        # go to working area
        rundir = 'run_%s' % run
        python_mkdir(rundir)
        os.chdir(rundir)

        tpeOut = 'TPEHists.root'
        valOut = {}
        valOut['All'] = 'valHists_run%s_%s.root' % (run, stream)
        for trigger in triggers:
            valOut[trigger] = '%s_valHists_run%s_%s.root' % (trigger, run, stream)
        csctfOut = 'csctfHist_run%s_%s.root' % (run, stream)

        # wait for job to finish then copy over
        print("Waiting on run %s" % run)
        while "Job <%s_%smerge> is not found" % (run,stream) not in subprocess.Popen("unbuffer bjobs -J %s_%smerge" % (run,stream), shell=True,stdout=pipe).communicate()[0].splitlines():
            time.sleep(20)
            print('.')
        else:
            print('.')
            print("Run %s merged" % run) 
            subprocess.call('cmsStage -f /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s %s' % (stream, run, eventContent, tpeOut, tpeOut), shell=True)
            valRet = subprocess.call('cmsStage -f /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s %s' % (stream, run, eventContent, valOut['All'], valOut['All']), shell=True)
            for trigger in triggers:
                trigRet = subprocess.call('cmsStage -f /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s %s' % (stream, run, eventContent, valOut[trigger], valOut[trigger]), shell=True)
            subprocess.call('cmsStage -f /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s %s' % (stream, run, eventContent, csctfOut, csctfOut), shell=True)
            if not valRet and not dryRun: os.system("./secondStep.py")
            subprocess.call('rm *.root', shell=True)

        os.chdir('../')
        
    os.chdir('../')

    build_runlist()
        
    return 0

def build_runlist():
    print "Building runlist"
    curTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    os.system('bash /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/scripts/generateRunList.sh > %s_runlist.json; mv %s_runlist.json /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/js/runlist.json' % (curTime,curTime))
    # create last run json
    Time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    with open('lastrun.json','w') as file:
        file.write('var lastrun = {\n  "lastrun" : "%s"\n}\n' % Time)
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
    run = kwargs.pop('run',0)
    force = kwargs.pop('force',False)

    # get stream info
    [filler, stream, version, eventContent] = dataset.split('/')

    # setup working directory for stream
    python_mkdir(stream)
    os.system("cp das_client.py "+stream)

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

    # run each individual validation
    if run:
        num = subprocess.Popen("./das_client.py --limit=0 --query='summary dataset=%s run=%s | grep summary.nevents'" % (dataset,str(run)), shell=True,stdout=pipe).communicate()[0].rstrip()
        procString = '%s_%s' % (str(run),num)
        if procString not in procRuns or force:
            if force: print "Forcing reprocessing"
            print "Processing run %s" % str(run)
            with open(procFile, 'a') as file:
                file.write(procString+'\n')
            run_validation(dataset,globalTag,str(run),stream,eventContent,force=force,**kwargs)
    else:
        # query DAS and get list of runs
        print "Querying DAS"
        newruns = subprocess.Popen("./das_client.py --query='run dataset="+dataset+"' --limit=0", shell=True, stdout=pipe).communicate()[0].splitlines()
        #newruns = get_data('https://cmsweb.cern.ch', "run dataset="+dataset, 0, 0, 0, 300, '', '')
        print "Available runs"
        print newruns
        for rn in newruns:
            try:
                _ = int(rn)
            except:
                print 'Not an int: %s' % rn
                continue
            if int(rn)<MINRUN: continue
            print 'Checking %s' %rn
            num = subprocess.Popen("./das_client.py --limit=0 --query='summary dataset=%s run=%s | grep summary.nevents'" % (dataset,rn), shell=True,stdout=pipe).communicate()[0].rstrip()
            try:
                _ = int(num)
            except:
                print 'Not an int: %s' % num
            print 'Num events: %s' % num
            procString = '%s_%s' % (rn, num)
            if procString in procRuns and not force: continue # already processed
            with open(procFile, 'a') as file:
                file.write(procString+'\n')
            if int(num) > 25000: # only care about long runs
                print "Processing run %s" % rn
                run_validation(dataset,globalTag,str(rn),stream,eventContent,force=force,**kwargs)

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
        process_output(args.dataset, args.globalTag, force=args.force, run=args.runNumber,triggers=args.triggers,dryRun=args.dryRun)
        return 0

    #if args.reprocessHistograms:
    #    return 0

    process_dataset(args.dataset, args.globalTag, run=args.runNumber, force=args.force,triggers=args.triggers,dryRun=args.dryRun)
    
    return 0

if __name__ == "__main__":
    main()
