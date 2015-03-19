#!/bin/bash
aklog

source /afs/cern.ch/cms/cmsset_default.sh

eval `scramv1 runtime -sh`
scram b

./run_cscval.py /ExpressCosmics/Commissioning2015-Express-v1/FEVT GR_E_V42
