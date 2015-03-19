#! /usr/bin/env python

# CSC Validation submit script
#   Primary submission script for CSCValidation processing. Outputs are available
#   at http://cms-project-csc-validation.web.cern.ch/cms-project-csc-validation/
#
# Authors
#   Ben Knapp, Northeastern University
#   Devin Taylor, UW-Madison

# Change Log
#
#   2015-03-18 - Devin Taylor
#    - crab won't submit to CAF, back to batch
#
#   2015-03-17 - Devin Taylor
#    - Moving to crab submission (break batch submission)
#    - Adding argparse module
#    - Adding FEVT for ExpressCosmics
#
#   2014-06-24 - Ben Knapp
#    - DAS queries
#    - Generate runlist from 'results' directory
#    - Retrieve 'nEvents' from DAS piping
#    - Options for local+batch (copy locally) or crab submission (later)
#    - Options for localruns, including whether '.raw' needs to be processed (to be added later)
#    - Modify directories to be hardcoded, along with more transparency


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

pipe = subprocess.PIPE
Release = subprocess.Popen('echo $CMSSW_VERSION', shell=True, stdout=pipe).communicate()[0]
Release = Release.rstrip("\n")

########## Directories #############

TEMPLATE_PATH = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/TEMPLATES_batch/'
RESULT_PATH = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/results/'
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

def replace(map, fileInName, fileOutName):
    '''Replace template file parameters'''
    replace_items = map.items()
    open(fileOutName,'w').close()
    with open(fileInName,'r') as filein:
        for line in filein:
            for old, new in replace_items:
                line = string.replace(line, old, new)
            with open(fileOutName,'a') as fileout:
                fileout.write(line)

################################
##### Validation functions #####
################################
def run_validation(dataset,globalTag,run,stream,eventContent):
    '''
    The primary validation routine. Creates working directories and submits jobs to crab.
    '''
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
    else:
        cfg  = 'cfg_noDigis_%s_template' % eventContent
        crab = 'crab_noDigis_%s_template' % eventContent
        proc = 'secondStep_noDigis_template'

    print "Will run with options: digis: %r standalone: %r" % (paramMap[eventContent]['digis'], paramMap[eventContent]['standalone'])

    templatecfgFilePath = TEMPLATE_PATH+cfg
    templatecrabFilePath = TEMPLATE_PATH+crab
    templateHTMLFilePath = TEMPLATE_PATH+"html_template"
    templateRootMacroPath = TEMPLATE_PATH+"makePlots.C"
    templateSecondStepPath = TEMPLATE_PATH+proc

    # get number of events in run
    num = subprocess.Popen("./das_client.py --limit=0 --query='summary dataset=%s run=%s | grep summary.nevents'" % (dataset,run), shell=True,stdout=pipe).communicate()[0].rstrip()
    nfiles = subprocess.Popen("./das_client.py --limit=0 --query='summary dataset=%s run=%s | grep summary.nfiles'" % (dataset,run), shell=True,stdout=pipe).communicate()[0].rstrip()
    nlumis = subprocess.Popen("./das_client.py --limit=0 --query='summary dataset=%s run=%s | grep summary.nlumis'" % (dataset,run), shell=True,stdout=pipe).communicate()[0].rstrip()

    print "Processing %s files, %s lumis, and %s events" % (nfiles, nlumis, num)

    # old HTML stuff, kept for backwards compatibility
    cfgFileName='validation_'+run+'_cfg.py'
    crabFileName='crab_'+run+'_cfg.py'
    htmlFileName = "Summary.html"
    macroFileName = "makePlots.C"
    procFileName = "secondStep.py"
    outFileName='valHists_run'+run+'_'+stream+'.root'
    Time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

    symbol_map_html = { 'RUNNUMBER':run, 'NEVENT':num, "DATASET":dataset, "CMSSWVERSION":Release, "GLOBALTAG":globalTag, "DATE":Time }
    symbol_map_macro = { 'FILENAME':outFileName }
    symbol_map_proc = { 'OUTPUTFILE':outFileName, 'RUNNUMBER':run, 'NEWDIR':rundir, 'CFGFILE':cfgFileName, 'STREAM':stream }
    symbol_map_cfg = { 'NEVENT':num, 'GLOBALTAG':globalTag, "OUTFILE":outFileName, 'DATASET':dataset, 'RUNNUMBER':run}
    symbol_map_crab = { 'GLOBALTAG':globalTag, "OUTFILE":outFileName, 'DATASET':dataset, 'RUNNUMBER':run, 'STREAM':stream, 'EVENTCONTENT':eventContent}

    replace(symbol_map_html,templateHTMLFilePath, htmlFileName)
    replace(symbol_map_macro,templateRootMacroPath, macroFileName)
    replace(symbol_map_proc,templateSecondStepPath, procFileName)
    replace(symbol_map_cfg,templatecfgFilePath, cfgFileName)
    replace(symbol_map_crab,templatecrabFilePath, crabFileName)

    os.system("chmod 755 secondStep.py")

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
        numFilesPerJob = float(10)
        numJobs = int(math.ceil(len(input_files)/numFilesPerJob))
        for j in range(numJobs):
            cfgFileName='validation_%s_%i_cfg.py' % (run, j)
            outFileName='valHists_run%s_%s_%i.root' % (run, stream, j)

            fileListString = ''
            numLumis = 0
            numEvents = 0
            for f in input_files[j*10:j*10+10]:
                if fileListString: fileListString += ',\n'
                fileListString += "    '%s'" % f

            symbol_map_cfg = { 'NEVENT':num, 'GLOBALTAG':globalTag, "OUTFILE":outFileName, 'DATASET':dataset, 'RUNNUMBER':run, 'FILELIST': fileListString, 'VERSION': str(j)}
            replace(symbol_map_cfg,templatecfgFilePath, cfgFileName)

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
            sh.write('cmsStage %s /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (outFileName, stream, run, eventContent, outFileName))
            sh.write('cmsStage TPEHists_%i.root /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/TPEHists_%i.root\n' % (j, stream, run, eventContent, j))
            sh.close()

            print "Submitting job %i of %i" % (j+1, numJobs)
            subprocess.check_call("bsub -q 8nh -J %s_%i < run_%i.sh" % (run, j, j), shell=True)

    os.chdir('../')

    return 0

def process_output(dataset,globalTag,**kwargs):
    '''
    Script to retrieve the crab output from EOS, merge the histograms, and create the images.
    '''
    [filler, stream, version, eventContent] = dataset.split('/')
    os.chdir(stream)

    runCrab = False

    runsToPlot = []
    # get available runs in eos
    for job in subprocess.Popen('/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls %s/%s' % (CRAB_PATH if runCrab else BATCH_PATH,stream), shell=True,stdout=pipe).communicate()[0].splitlines():
        # go to working area
        if runCrab:
            [type, runStr, runEventContent] = job.split('_')
        else: 
            [runStr,runEventContent] = job.split('_')
        run = runStr[3:]

        # some job still running. skip.
        if "Job <"+run+"*> is not found" not in subprocess.Popen("unbuffer bjobs -J "+run+"*", shell=True,stdout=pipe).communicate()[0].splitlines():
            print 'Run %s not finished' % run
            continue

        rundir = 'run_%s' % run
        python_mkdir(rundir)
        os.chdir(rundir)

        tpeOut = 'TPEHists.root'
        valOut = 'valHists_run%s_%s.root' % (run, stream)

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
        valFiles = []
        for file in subprocess.Popen('/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls %s' % (fileDir), shell=True,stdout=pipe).communicate()[0].splitlines():
            if file==tpeOut or file==valOut: continue
            if file[0:3]=='TPE': tpeFiles += [file]
            if file[0:3]=='val': valFiles += [file]
        nFiles = len(valFiles)

        # see if we need to remerge things
        processedString = '%s_%i' %(jobVersion, nFiles)
        fname = 'out.txt'
        open(fname, 'a').close()
        with open(fname,'r') as file:
            oldProcessedString = file.readline().rstrip()

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
        if valFiles:
            print "Merging valHists"
            valMergeString = 'hadd -f %s' % valOut
            for val in valFiles:
                valMergeString += ' root://eoscms.cern.ch/%s/%s' % (fileDir, val)
            sh.write(valMergeString+" \n")
        sh.write('cmsStage -f %s /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (tpeOut, stream, run, eventContent, tpeOut))
        sh.write('cmsStage -f %s /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s\n' % (valOut, stream, run, eventContent, valOut))
        sh.close()
        subprocess.check_call("bsub -q 8nh -J "+run+"merge"+" < merge.sh", shell=True)

        runsToPlot += [[run,job]]

        os.chdir('../')

    # now plot the merges as they finish
    for run,job in runsToPlot:
        # go to working area
        rundir = 'run_%s' % run
        python_mkdir(rundir)
        os.chdir(rundir)

        tpeOut = 'TPEHists.root'
        valOut = 'valHists_run%s_%s.root' % (run, stream)

        # wait for job to finish then copy over
        print("Waiting on run %s" % run)
        while "Job <"+run+"merge> is not found" not in subprocess.Popen("unbuffer bjobs -J "+run+"merge", shell=True,stdout=pipe).communicate()[0].splitlines():
            time.sleep(20)
            print('.')
        else:
            print('.')
            print("Run %s merged" % run) 
            subprocess.check_call('cmsStage -f /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s %s' % (stream, run, eventContent, tpeOut, tpeOut), shell=True)
            subprocess.check_call('cmsStage -f /store/group/dpg_csc/comm_csc/cscval/batch_output/%s/run%s_%s/%s %s' % (stream, run, eventContent, valOut, valOut), shell=True)
            os.system("./secondStep.py")
            subprocess.call('rm *.root', shell=True)

        os.chdir('../')
        
    os.chdir('../')

    build_runlist()
        
    return 0

def build_runlist():
    print "Building runlist"
    os.system('bash /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/scripts/generateRunList.sh > runlist.json; mv runlist.json /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/js/')

def process_dataset(dataset,globalTag,**kwargs):
    '''
    Script to call validation of multiple runs
      kwargs:
        argument    type    default    comment
        run         int     0          if nonzero, will process a single run, else, process all available
    '''
    run = kwargs.pop('run',0)

    # get stream info
    [filler, stream, version, eventContent] = dataset.split('/')

    # setup working directory for stream
    python_mkdir(stream)
    os.system("cp das_client.py "+stream)

    # begin running
    start=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    print "CSCVal job inititiated at "+start
    os.chdir(stream)

    procFile = 'processedRuns.txt'
    open(procFile, 'a').close()
    with open(procFile, 'r') as file:
        procRuns = file.readlines()
    procRuns = [x.rstrip() for x in procRuns]

    # run each individual validation
    if run:
        if str(run) not in procRuns:
            print "Processing run %s" % str(run)
            with open(procFile, 'a') as file:
                file.write(str(run)+'\n')
            run_validation(dataset,globalTag,str(run),stream,eventContent)
    else:
        # query DAS and get list of runs
        newruns = subprocess.Popen("./das_client.py --query='run dataset="+dataset+"' --limit=0", shell=True, stdout=pipe).communicate()[0].splitlines()
        for rn in newruns:
            if int(rn)<237956: continue # start from here
            if rn in procRuns: continue # already processed
            with open(procFile, 'a') as file:
                file.write(rn+'\n')
            processRun = True
            if 'run_'+rn in os.listdir('.'):
                processRun = False # we already created the crab job
            if 'run'+rn in os.listdir(RESULT_PATH):
                if stream in os.listdir('%s/%s' %(RESULT_PATH,'run'+rn)):
                    processRun = False # someone else already processed this stream
            if processRun:
                print "Processing run %s" % rn
                num = subprocess.Popen("./das_client.py --limit=0 --query='summary dataset=%s run=%s | grep summary.nevents'" % (dataset,rn), shell=True,stdout=pipe).communicate()[0].rstrip()
                if int(num) > 50000: # only care about long runs
                    run_validation(dataset,globalTag,str(rn),stream,eventContent)

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

    args = parser.parse_args(argv)
    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_command_line(argv)

    ds = args.dataset.split('/')
    if len(ds) != 4: 
        print 'Invalid dataset. Argument should be in the form of a DAS query (/*/*/*).'
        return 0

    if args.buildRunlist:
        build_runlist()
        return 0

    if args.retrieveOutput:
        process_output(args.dataset, args.globalTag)
        return 0

    #if args.reprocessHistograms:
    #    return 0

    process_dataset(args.dataset, args.globalTag, run=args.runNumber)
    
    return 0

if __name__ == "__main__":
    main()
