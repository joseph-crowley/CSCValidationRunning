#!/bin/bash
aklog

echo "Setup environment"

source /afs/cern.ch/cms/cmsset_default.sh

cd /afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/AUTOVAL/CMSSW_7_3_5/src/CSCValidationRunning/AutoValidation

eval `scramv1 runtime -sh`
scram b

echo "Initiate validation script"

#cern-get-sso-cookie --krb -r -u https://cmswbm.web.cern.ch/cmswbm/cmsdb/servlet/RunSummary -o ~/private/ssocookie.txt
./run_cscval.py /Cosmics/Commissioning2015-v1/RAW GR_P_V50 -t HLT_L1SingleMuOpen_v6 HLT_L1SingleMuBeamHalo_v1
