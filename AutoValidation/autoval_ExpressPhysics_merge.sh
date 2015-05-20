#!/bin/bash
aklog

echo "Setup environment"
source /afs/cern.ch/cms/cmsset_default.sh

cd /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_7_4_2/src/CSCValidationRunning/AutoValidation

eval `scramv1 runtime -sh`
scram b

echo "Initiate merge script"
./run_cscval.py /ExpressPhysics/Commissioning2015-Express-v1/FEVT GR_E_V47 -ro -t HLT_L1SingleMuOpen_WideWindow_v1
