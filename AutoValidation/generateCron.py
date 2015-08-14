#!/usr/bin/env python

import sys
import os
import math
import stat

def chmodX(filename):
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)

def generate():
    cronName = 'autoval'
    datasets = {
        '/ExpressPhysics/Run2015C-Express-v1/FEVT' : {
            'globaltag' : '74X_dataRun2_Express_v1',
        },
        '/ExpressCosmics/Run2015C-Express-v1/FEVT' : {
            'globaltag' : '74X_dataRun2_Express_v1',
        },
        '/SingleMuon/Run2015C-v1/RAW' : {
            'globaltag' : '74X_dataRun2_Prompt_v1',
        },
        '/Cosmics/Run2015C-v1/RAW' : {
            'globaltag' : '74X_dataRun2_Prompt_v1',
        },
    }
    
    CMSSW_BASE = os.environ.get('CMSSW_BASE')
    if not CMSSW_BASE: return

    commandString = '#!/bin/bash\n'
    commandString += 'aklog\n'
    commandString += 'echo "Setup environment"\n'
    commandString += 'source /afs/cern.ch/cms/cmsset_default.sh\n'
    commandString += 'cd %s/src/CSCValidationRunning/AutoValidation\n' % CMSSW_BASE
    commandString += 'eval `scramv1 runtime -sh`\n'
    commandString += 'scram b\n'
    commandString += 'echo "Initiate validation script"\n'

    with open('{0}.cron'.format(cronName),'w') as f:
        f.write('')

    for dataset in datasets:
        globaltag = datasets[dataset]['globaltag']
        dummy, datasetName, periodName, eventContent = dataset.split('/')
        filename = '%s_%s-%s-%s' % (cronName, datasetName, periodName, eventContent)
        mergeFilename = '{0}_merge'.format(filename)
        commandToWrite = commandString + './run_cscval.py %s %s\n' % (dataset, globaltag)
        mergeCommandToWrite = commandString + './run_cscval.py %s %s -ro\n' % (dataset, globaltag)
        acrontabString = '1 * * * * lxplus.cern.ch {0}/src/CSCValidationRunning/AutoValidation/{1}.sh >> {0}/src/CSCValidationRunning/AutoValidation/{1}.log 2>> {0}/src/CSCValidationRunning/AutoValidation/{1}.err\n'.format(CMSSW_BASE,filename)
        acrontabMergeString = '31 * * * * lxplus.cern.ch {0}/src/CSCValidationRunning/AutoValidation/{1}.sh >> {0}/src/CSCValidationRunning/AutoValidation/{1}.log 2>> {0}/src/CSCValidationRunning/AutoValidation/{1}.err\n'.format(CMSSW_BASE,mergeFilename)
        with open('{0}.sh'.format(filename),'w') as f:
            f.write(commandToWrite)
        chmodX('{0}.sh'.format(filename))
        with open('{0}.sh'.format(mergeFilename),'w') as f:
            f.write(mergeCommandToWrite)
        chmodX('{0}.sh'.format(mergeFilename))
        with open('{0}.cron'.format(cronName),'a') as f:
            f.write(acrontabString)
            f.write(acrontabMergeString)
        

generate()
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    generate()


if __name__ == "__main__":
    main()
             
