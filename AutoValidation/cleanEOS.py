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
from dbs.apis.dbsClient import DbsApi

MAXRUN = 283835 # after move to dbs

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

def remove(**kwargs):
    '''
    Script to retrieve the output from EOS, merge the histograms, and create the images.
    '''
    dryRun = kwargs.pop('dryRun',False)

    # get available runs in eos
    for stream in subprocess.Popen('/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls %s' % (BATCH_PATH), shell=True,stdout=pipe).communicate()[0].splitlines():
        print 'Cleaning {0}'.format(stream)
        for job in subprocess.Popen('/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls %s/%s' % (BATCH_PATH,stream), shell=True,stdout=pipe).communicate()[0].splitlines():
            print 'Cleaning {0}'.format(job)
            [runStr,runEventContent] = job.split('_')
            run = runStr[3:]
            if int(run)>MAXRUN: continue

            tpeOut = 'TPEHists.root'
            valOut = {}
            valOut['All'] = 'valHists_run%s_%s.root' % (run, stream)
            csctfOut = 'csctfHist_run%s_%s.root' % (run, stream)

            jobVersion = 'job'
            fileDir = '%s/%s/%s' % (BATCH_PATH,stream,job)
            tpeFiles = []
            valFiles = {}
            valFiles['All'] = []
            csctfFiles = []
            for file in subprocess.Popen('/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls %s' % (fileDir), shell=True,stdout=pipe).communicate()[0].splitlines():
                if file==tpeOut or file==valOut or file==csctfOut: continue
                if file[0:3]=='TPE': tpeFiles += [file]
                if file[0:3]=='val': valFiles['All'] += [file]
                if file[0:5]=='csctf': csctfFiles += [file]
            nFiles = len(valFiles['All'])

            # and delete them
            if tpeFiles:
                for tpe in tpeFiles:
                    if tpe==tpeOut: continue # skip previous merge
                    command = '/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select rm %s/%s' % (fileDir, tpe)
                    if dryRun:
                        print command
                    else:
                        result = subprocess.Popen(command, shell=True,stdout=pipe).communicate()[0]
                        if result: print result
            if valFiles['All']:
                for val in valFiles['All']:
                    if val==valOut['All']: continue # skip previous merge
                    command = '/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select rm %s/%s' % (fileDir, val)
                    if dryRun:
                        print command
                    else:
                        result = subprocess.Popen(command, shell=True,stdout=pipe).communicate()[0]
                        if result: print result
            if csctfFiles:
                for csctf in csctfFiles:
                    if csctf==csctfOut: continue # skip previous merge
                    command = '/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select rm %s/%s' % (fileDir, csctf)
                    if dryRun:
                        print command
                    else:
                        result = subprocess.Popen(command, shell=True,stdout=pipe).communicate()[0]
                        if result: print result


    return 0

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description="A script to clean up the unmerged files after we are doing running over that dataset.")

    
    parser.add_argument('-dr', '--dryRun', action='store_true',help='Don\'t submit')

    args = parser.parse_args(argv)
    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_command_line(argv)

    remove(dryRun=args.dryRun)

    return 0

if __name__ == "__main__":
    main()
