#!/bin/bash

# runDir=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/results
runDir=${1:-/eos/cms/store/group/dpg_csc/comm_csc/cscval/www/results}
allRuns=$runDir/run[0-9][0-9][0-9][0-9][0-9][0-9]
#allRuns=$runDir/run207[0-9][0-9][0-9]
echo "var runData = {"
output=""
for runPath in $allRuns
do
    if [ -n "$output" ]
    then
        output=","
    fi

    run=$(basename $runPath)
    run=${run:3:${#run}}

    datasets="$runPath/*"
    skipRun=true
    for datasetPath in $datasets
    do
        if [ -f $datasetPath/Site/PNGS/hORecHitsSerial.png ] ; then
            # no CSCs in run, don't show
            skipRun=false
        fi
    done
    if [ "$skipRun" = true ] ; then
        continue
    fi

    output="$output\n  \"$run\" : {"
    output="$output\n    \"directory\" : \"$run\","
    output="$output\n    \"datasets\" : {"
    for datasetPath in $datasets
    do
        if [ ! -f $datasetPath/Site/PNGS/hORecHitsSerial.png ] ; then
            # no CSCs in dataset
            continue
        fi
        dataset=$(basename $datasetPath)
        output="$output\n      \"$dataset\" : {"

        # now parse the file and get the summary values
        summaryFile=$datasetPath/Site/Summary.html  
        parsed=`lynx --nomargins --nolist --dump $summaryFile`
        parsed=${parsed//$'\n'/}
        release==${parsed%Dataset:*}
        release=${release##*Release: }
        datasetname==${parsed%Run:*}
        datasetname=${datasetname##*Dataset: }
        runnum==${parsed%# of Events Processed:*}
        runnum=${runnum##*Run: }
        events==${parsed%Using GlobalTag:*}
        events=${events##*# of Events Processed: }
        globaltag==${parsed%CSCValidation was run on *}
        globaltag=${globaltag##*GlobalTag: }
        rundate==${parsed%\"Dead\"*}
        rundate=${rundate##*CSCValidation was run on }

        output="$output\n        \"release\" : \"$release\","
        output="$output\n        \"datasetname\" : \"$datasetname\","
        output="$output\n        \"runnum\" : \"$runnum\","
        output="$output\n        \"events\" : \"$events\","
        output="$output\n        \"globaltag\" : \"$globaltag\","
        output="$output\n        \"rundate\" : \"$rundate\""
        output="$output\n      },"
    done
    # delete trailing ,
    output="${output%?}"
    output="$output\n    }"
    output="$output\n  }"
    printf "$output"
done
output="\n"
# for some reason the last } isnt printing
printf "$output"
echo "}"
