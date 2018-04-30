# CSCValidationRunning
Repository to setup the latest version of CSCValidation to be run automatically on CERN Analysis Facility (CAF)

## Setup

Setup a new release
```
cmsrel CMSSW_10_0_0_pre3 # or current CMSSW version
cd CMSSW_10_0_0_pre3/src
cmsenv
git cms-init # make sure this happens before checking out this repository
```

Clone the repository
```
git clone git@github.com:wsicheng/CSCValidationRunning.git
```

Run the setup script to add DQM/L1TMonitor 
and source CRAB3 setup for DbsApi client
```
cd CSCValidationRunning
./setup.sh
source /cvmfs/cms.cern.ch/crab3/crab.sh
```

## Starting cron job

To run a cron job on afs you must use acrontab. The current version crontab script is in
[AutoValidation/autoval.cron](AutoValidation/autoval.cron). Make certain you consult with others to make 
sure we don't have multiple cron jobs running. A schedule can be found at the [Twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/CSCValidationWebsite).
Note: DAS requires authentication.
To run with acrontab, do a `voms-proxy-init` and copy the `/tmp/x509up_uXXXX` file to a private directory on afs.
The /tmp directory will not be visible on all lxplus nodes (just the one you create it on).
```
python generateCron.py /path/to/proxy
acrontab <autoval.acron
acrontab -l
```

## Individual running

The primary submission script can be found in [AutoValidation/run_cscval.py](AutoValidation/run_cscval.py).

This script can run over multiple event content types (FEVT and RAW). You must simply pass it the 
dataset name and global tag. The script can be run in single run mode (`-rn RUNNUMBER`) or all runs mode. 
It will then check whether a run has been processed yet and whether CSCs were in the run and submit the 
job to the CAF LSF batch queues. After the job is finished, the outputs are stored on EOS. You can then 
produce the images and pass the output to the website with the `--retrieveOutput` option.

If you only want to submit a certain number of batch jobs (at present 1 batch job per LFN), check the option `-mj JOBNUM`, where JOBNUM is an integer. If this option is not checked, the current default max number of batch jobs is 200.

The script checks the local folder for what runs have been processed: `AutoValidation/STREAMNAME`. The 
`STREAMNAME` option can include `ExpressCosmics`, `Cosmics`, `SingleMu`, and `DoubleMu`.

## Templates

Templates for producing the scripts to submit to bash are found in the [Templates](Templates) directory.


## Some tips

* To make the stderr output files `*_merge.err` more readable, one can put the following line
```
Root.ErrorIgnoreLevel: Error
```
into their `~/.rootrc` , to suppress the infinite "TCanvas::Print" statments.
