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
        # Run2015D Express v3
        #'/ExpressPhysics/Run2015D-Express-v3/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/ExpressPhysics_0T/Run2015D-Express-v3/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/ExpressCosmics/Run2015D-Express-v3/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        # Run2015D Express v4
        #'/ExpressPhysics/Run2015D-Express-v4/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/ExpressPhysics_0T/Run2015D-Express-v4/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/ExpressCosmics/Run2015D-Express-v4/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        # Run2015E Express v1
        #'/ExpressPhysics/Run2015E-Express-v1/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/HIExpressPhysics/Run2015E-Express-v1/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/ExpressPhysics_0T/Run2015E-Express-v1/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/HIExpressPhysics_0T/Run2015E-Express-v1/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/ExpressCosmics/Run2015E-Express-v1/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        # HIRun2015
        #'/ExpressPhysics/HIRun2015-Express-v1/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/HIExpressPhysics/HIRun2015-Express-v1/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/ExpressPhysics_0T/HIRun2015-Express-v1/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/HIExpressPhysics_0T/HIRun2015-Express-v1/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        #'/ExpressCosmics/HIRun2015-Express-v1/FEVT' : {
        #    'globaltag' : '74X_dataRun2_Express_v1',
        #},
        # Commissioning2016 Express
        #'/ExpressCosmics/Commissioning2016-Express-v1/FEVT' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        #'/ExpressPhysics/Commissioning2016-Express-v1/FEVT' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        # Run2016A Express
        #'/ExpressCosmics/Run2016A-Express-v1/FEVT' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        #'/ExpressPhysics/Run2016A-Express-v1/FEVT' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        #'/ExpressCosmics/Run2016A-Express-v2/FEVT' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        #'/ExpressPhysics/Run2016A-Express-v2/FEVT' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        # Run2016B Express
        #'/ExpressCosmics/Run2016B-Express-v1/FEVT' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        #'/ExpressPhysics/Run2016B-Express-v1/FEVT' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        '/ExpressCosmics/Run2016B-Express-v2/FEVT' : {
            'globaltag' : 'auto:run2_data',
        },
        '/ExpressPhysics/Run2016B-Express-v2/FEVT' : {
            'globaltag' : 'auto:run2_data',
        },

        # Run2015D RAW
        #'/SingleMuon/Run2015D-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/SingleMuon_0T/Run2015D-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/Cosmics/Run2015D-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        # Run2015E RAW
        #'/SingleMuon/Run2015E-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/DoubleMuon/Run2015E-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/SingleMuon_0T/Run2015E-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/SingleMuLowPt/Run2015E-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/SingleMuHighPt/Run2015E-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/DoubleMu/Run2015E-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/HIPhysicsMuon/Run2015E-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/Cosmics/Run2015E-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        # HIRun2015
        #'/SingleMuon/HIRun2015-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/DoubleMuon/HIRun2015-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/SingleMuon_0T/HIRun2015-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/SingleMuLowPt/HIRun2015-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/SingleMuHighPt/HIRun2015-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/DoubleMu/HIRun2015-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/HIPhysicsMuon/HIRun2015-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        #'/Cosmics/HIRun2015-v1/RAW' : {
        #    'globaltag' : '74X_dataRun2_Prompt_v1',
        #},
        # Commissioning2016
        #'/Cosmics/Commissioning2016-v1/RAW' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        # Run2016A
        #'/Cosmics/Run2016A-v1/RAW' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        # Run2016B
        #'/Cosmics/Run2016B-v1/RAW' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        #'/SingleMuon/Run2016B-v1/RAW' : {
        #    'globaltag' : 'auto:run2_data',
        #},
        '/Cosmics/Run2016B-v2/RAW' : {
            'globaltag' : 'auto:run2_data',
        },
        '/SingleMuon/Run2016B-v2/RAW' : {
            'globaltag' : 'auto:run2_data',
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
             
