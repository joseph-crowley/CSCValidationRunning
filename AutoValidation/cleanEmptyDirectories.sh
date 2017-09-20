#!/bin/bash

BASEDIR=/eos/cms/store/group/dpg_csc/comm_csc/cscval/www/results
echo "listing directories in EOS www folder w/ no CSC information (no hORecHitsSerial.png)"
ls -l $BASEDIR/*/*/Site/PNGS/hORecHitsSerial.png |  sed -n -E "s/.*(run[0-9]*\/[a-zA-Z]*[^\/])\/.*/\1/p" | sort > hasCSC.txt
ls -l $BASEDIR/*/*/ |  sed -n -E "s/.*(run[0-9]*\/[a-zA-Z]*[^\/])\/.*/\1/p" | sort > allDirs.txt
comm -3 allDirs.txt hasCSC.txt > toRemove.txt
while read TOREMOVE; do
    echo "#rm -rf $BASEDIR/$TOREMOVE"
done < toRemove.txt
