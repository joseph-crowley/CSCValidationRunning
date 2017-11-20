#! /usr/bin/env python

# CSC Validation submit script
#   Primary submission script for CSCValidation processing. Outputs are available
#   at https://cms-conddb.cern.ch/eosweb/csc/
#
# Authors
#   Ben Knapp, Northeastern University
#   Devin Taylor, UW-Madison

######################################################
###############   Configuration   ####################
######################################################

import os
import sys
import string
import time
import subprocess
import argparse
import errno
import math

########## Constants #############

# only clean runs within this period
MINRUN = 290000 
MAXRUN = 304000

pipe = subprocess.PIPE
Release = subprocess.Popen('echo $CMSSW_VERSION', shell=True, stdout=pipe).communicate()[0]
Release = Release.rstrip("\n")
NPLOTS = 410
UID = os.getuid()

########## Directories #############

TEMPLATE_PATH = '%s/src/CSCValidationRunning/Templates' % os.environ['CMSSW_BASE']
RESULT_PATH = '/eos/cms/store/group/dpg_csc/comm_csc/cscval/www/results'
WWW_PATH = '/eos/cms/store/group/dpg_csc/comm_csc/cscval/www'
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

def check_nplots(runStr, stream, threshold=20):
    '''Check that enough number of plots already exist at the website'''
    plotDir = RESULT_PATH + '/' + runStr + '/' + stream + '/Site/PNGS'
    if not os.path.exists(plotDir): 
        return False
    nPlots = len(os.listdir(plotDir))
    if nPlots < NPLOTS - threshold:
        print '%s has %s plots, does not meet the expected number %s, will hold off from cleaning it.' % (runStr, nPlots, NPLOTS)
        return False
    else:
        return True

#####################
##### Utilities #####
#####################
def remove(**kwargs):
    '''
    Script to retrieve the output from EOS, merge the histograms, and create the images.
    '''
    dryRun = kwargs.pop('dryRun',False)

    # get available runs in eos
    # for stream in subprocess.Popen('ls %s' % (BATCH_PATH), shell=True,stdout=pipe).communicate()[0].splitlines():
    for stream in ['SingleMuon', 'DoubleMuon', 'ExpressPhysics', 'ExpressCosmics']:
    # for stream in [ 'SingleMuon']:
        print 'Cleaning {0}'.format(stream)
        for job in subprocess.Popen('ls %s/%s' % (BATCH_PATH,stream), shell=True,stdout=pipe).communicate()[0].splitlines():
            [runStr,runEventContent] = job.split('_')
            run = runStr[3:]
            if int(run) < MINRUN: continue
            if int(run) > MAXRUN: continue
            if not check_nplots(runStr, stream): continue

            print 'Cleaning {0}'.format(job)

            tpeOut = 'TPEHists.root'
            valOut = {}
            valOut['All'] = 'valHists_run%s_%s.root' % (run, stream)
            csctfOut = 'csctfHist_run%s_%s.root' % (run, stream)
            emtfOut = 'emtfHist_run%s_%s.root' % (run, stream)

            jobVersion = 'job'
            fileDir = '%s/%s/%s' % (BATCH_PATH,stream,job)
            tpeFiles = []
            valFiles = {}
            valFiles['All'] = []
            csctfFiles = []
            emtfFiles = []
            for file in subprocess.Popen('ls %s' % (fileDir), shell=True,stdout=pipe).communicate()[0].splitlines():
                if file==tpeOut or file==valOut or file==csctfOut or file==emtfOut: continue
                if file[0:3]=='TPE': tpeFiles += [file]
                if file[0:3]=='val': valFiles['All'] += [file]
                if file[0:5]=='csctf': csctfFiles += [file]
                if file[0:4]=='emtf': emtfFiles += [file]
            nFiles = len(valFiles['All'])

            # and delete them
            if tpeFiles:
                for tpe in tpeFiles:
                    if tpe==tpeOut: continue # skip previous merge
                    command = '%s/%s' % (fileDir, tpe)
                    if os.stat(command) == UID:
                        command = 'rm ' + command
                    else:
                        command = 'printf "" > ' + command
                    if dryRun:
                        print command
                    else:
                        result = subprocess.Popen(command, shell=True,stdout=pipe).communicate()[0]
                        if result: print result
            if valFiles['All']:
                for val in valFiles['All']:
                    if val==valOut['All']: continue # skip previous merge
                    command = '%s/%s' % (fileDir, val)
                    if os.stat(command) == UID:
                        command = 'rm ' + command
                    else:
                        command = 'printf "" > ' + command
                    if dryRun:
                        print command
                    else:
                        result = subprocess.Popen(command, shell=True,stdout=pipe).communicate()[0]
                        if result: print result
            if csctfFiles:
                for csctf in csctfFiles:
                    if csctf==csctfOut: continue # skip previous merge
                    command = '%s/%s' % (fileDir, csctf)
                    if os.stat(command) == UID:
                        command = 'rm ' + command
                    else:
                        command = 'printf "" > ' + command
                    if dryRun:
                        print command
                    else:
                        result = subprocess.Popen(command, shell=True,stdout=pipe).communicate()[0]
                        if result: print result
            if emtfFiles:
                for emtf in emtfFiles:
                    if emtf==emtfOut: continue # skip previous merge
                    command = '%s/%s' % (fileDir, val)
                    if os.stat(command) == UID:
                        command = 'rm ' + command
                    else:
                        command = 'printf "" > ' + command
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
