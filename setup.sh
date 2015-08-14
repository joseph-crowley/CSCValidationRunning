#!/bin/bash

set -o errexit
set -o nounset

: ${CMSSW_BASE:?"CMSSW_BASE is not set! Run cmsenv before recipe.sh"}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`

echo "Detected CMSSW version: $MAJOR_VERSION $MINOR_VERSION"

pushd $CMSSW_BASE/src

git cms-addpkg DQM/L1TMonitor
ln -s CSCValidationRunning/RecoLocalMuon RecoLocalMuon

scram b -j 8

popd

echo "Now setup new crontab (did you remember to kill your old one?)."
