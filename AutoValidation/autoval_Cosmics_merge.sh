#!/bin/bash
aklog

echo "Setup environment"
source /afs/cern.ch/cms/cmsset_default.sh

cd /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_7_3_5/src/CSCValidationRunning/AutoValidation

eval `scramv1 runtime -sh`
scram b

echo "Initiate merge script"
./run_cscval.py /Cosmics/Commissioning2015-v1/RAW GR_P_V50 -ro
