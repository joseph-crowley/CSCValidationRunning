#!/usr/bin/env python

import sys
import os
import math
import stat

def chmodX(filename):
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)

def generate(userproxy=''):

    cronName = 'autoval'
    datasets = {
        # Run2017 Express, Commissioning & Cosmics
        # '/ExpressPhysics/Run2017A-Express-v1/FEVT' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/ExpressPhysics/Run2017A-Express-v2/FEVT' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/ExpressPhysics/Run2017A-Express-v3/FEVT' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/ExpressPhysics/Run2017B-Express-v1/FEVT' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/ExpressPhysics/Run2017B-Express-v2/FEVT' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/ExpressPhysics/Run2017C-Express-v2/FEVT' : {
        #    'globaltag' : 'auto:run2_data',
        # },
        # '/ExpressPhysics/Run2017C-Express-v3/FEVT' : {
        #    'globaltag' : 'auto:run2_data',
        # },
        # '/ExpressPhysics/Run2017D-Express-v1/FEVT' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/ExpressPhysics/Run2017E-Express-v1/FEVT' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/Commissioning/Run2017A-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/CommissioningMuons/Run2017A-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/Cosmics/Run2017A-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/Cosmics/Run2017B-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/Cosmics/Run2017C-v1/RAW' : {
        #    'globaltag' : 'auto:run2_data',
        # },
        # '/Cosmics/Run2017D-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/Cosmics/Run2017E-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # Run2017 PromptReco
        # '/SingleMuon/Run2017A-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/DoubleMuon/Run2017A-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/SingleMuon/Run2017B-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/DoubleMuon/Run2017B-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/SingleMuon/Run2017C-v1/RAW' : {
        #    'globaltag' : 'auto:run2_data',
        # },
        # '/DoubleMuon/Run2017C-v1/RAW' : {
        #    'globaltag' : 'auto:run2_data',
        # },
        # '/SingleMuon/Run2017D-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/DoubleMuon/Run2017D-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/SingleMuon/Run2017E-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/DoubleMuon/Run2017E-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/SingleMuon/Run2017F-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        # '/DoubleMuon/Run2017F-v1/RAW' : {
        #     'globaltag' : 'auto:run2_data',
        # },
        '/SingleMuon/Run2018A-v1/RAW' : {
            'globaltag' : 'auto:run2_data',
        },
        '/DoubleMuon/Run2018A-v1/RAW' : {
            'globaltag' : 'auto:run2_data',
        },
        '/ExpressPhysics/Run2018A-Express-v1/FEVT' : {
            'globaltag' : 'auto:run2_data',
        },
        
    }
    
    CMSSW_BASE = os.environ.get('CMSSW_BASE')
    if not CMSSW_BASE: return

    commandString = '#!/bin/bash\n'
    commandString += 'aklog\n'
    commandString += 'echo "Setup environment"\n'
    commandString += 'source /etc/bashrc\n'
    commandString += 'source /afs/cern.ch/cms/cmsset_default.sh\n'
    commandString += 'cd %s/src/CSCValidationRunning/AutoValidation\n' % CMSSW_BASE
    commandString += 'eval `scramv1 runtime -sh`\n'
    commandString += 'source /cvmfs/cms.cern.ch/crab3/crab.sh\n'
    # commandString += 'scram b\n'
    if userproxy: commandString += 'export X509_USER_PROXY={0}\n'.format(userproxy)

    with open('{0}.acron'.format(cronName),'w') as f:
        f.write('')

    with open('{0}.cron'.format(cronName),'w') as f:
        f.write('')

    with open('{0}.sh'.format(cronName),'w') as f:
        f.write('')

    with open('{0}_merge.sh'.format(cronName),'w') as f:
        f.write('')

    for dataset in datasets:
        globaltag = datasets[dataset]['globaltag']
        dummy, datasetName, periodName, eventContent = dataset.split('/')
        filename = '%s_%s-%s-%s' % (cronName, datasetName, periodName, eventContent)
        mergeFilename = '{0}_merge'.format(filename)
        timeString  = 'echo "[$(date)] Initiate validation for %s"\n' % (dataset)
        timeString += 'echo "[$(date)] Initiate validation for %s" >&2\n' % (dataset)
        runVal = './run_cscval.py -mj 100 %s %s\n' % (dataset, globaltag)
        commandToWrite = commandString + timeString + runVal
        runMerge = './run_cscval.py %s %s -ro\n' % (dataset, globaltag)
        mergeCommandToWrite = commandString + timeString + runMerge
        acrontabString = '1 3,15 * * * lxplus.cern.ch {0}/src/CSCValidationRunning/AutoValidation/{1}.sh >> {0}/src/CSCValidationRunning/AutoValidation/{1}.log 2>> {0}/src/CSCValidationRunning/AutoValidation/{1}.err\n'.format(CMSSW_BASE,filename)
        acrontabMergeString = '31 7,19 * * * lxplus.cern.ch {0}/src/CSCValidationRunning/AutoValidation/{1}.sh >> {0}/src/CSCValidationRunning/AutoValidation/{1}.log 2>> {0}/src/CSCValidationRunning/AutoValidation/{1}.err\n'.format(CMSSW_BASE,mergeFilename)
        crontabString = '1 3,15 * * * {0}/src/CSCValidationRunning/AutoValidation/{1}.sh >> {0}/src/CSCValidationRunning/AutoValidation/{1}.log 2>> {0}/src/CSCValidationRunning/AutoValidation/{1}.err\n'.format(CMSSW_BASE,filename)
        crontabMergeString = '31 7,19 * * * {0}/src/CSCValidationRunning/AutoValidation/{1}.sh >> {0}/src/CSCValidationRunning/AutoValidation/{1}.log 2>> {0}/src/CSCValidationRunning/AutoValidation/{1}.err\n'.format(CMSSW_BASE,mergeFilename)
        with open('{0}.sh'.format(filename),'w') as f:
            f.write(commandToWrite)
        with open('{0}.sh'.format(cronName),'a') as f:
            f.write(runVal)
        chmodX('{0}.sh'.format(filename))
        with open('{0}.sh'.format(mergeFilename),'w') as f:
            f.write(mergeCommandToWrite)
        with open('{0}_merge.sh'.format(cronName),'a') as f:
            f.write(runMerge)
        chmodX('{0}.sh'.format(mergeFilename))
        with open('{0}.acron'.format(cronName),'a') as f:
            f.write(acrontabString)
            f.write(acrontabMergeString)
        with open('{0}.cron'.format(cronName),'a') as f:
            f.write(crontabString)
            f.write(crontabMergeString)
        
    chmodX('{0}.sh'.format(cronName))
    chmodX('{0}_merge.sh'.format(cronName))

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if not len(argv):
        print 'Note: you will not be able to submit acrontab jobs without a userproxy'
        generate()
    else:
        if not os.path.isfile(argv[0]):
            print 'You must provide a valid user proxy file: {0} invalid'.format(userproxy)
            return
        generate(argv[0])


if __name__ == "__main__":
    main()
             
