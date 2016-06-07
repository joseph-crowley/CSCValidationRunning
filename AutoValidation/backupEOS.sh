#!/bin/bash

for i in $( ls /afs/cern.ch/cms/caf/cafeos/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/results/ )
do
	goodRun=true
	for j in $( /afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select ls /eos/cms/store/group/dpg_csc/comm_csc/cscval/www/results/ )
	do
		if [ "$i" == "$j" ]
		then
			goodRun=false
		fi
	done
	if [ "$goodRun" == true ]
	then
		#copy
		src=/afs/cern.ch/cms/caf/cafeos/CAF/CMSCOMM/COMM_CSC/CSCVAL/results/results/
		dest=/eos/cms/store/group/dpg_csc/comm_csc/cscval/www/results/$i/
		tarfile=$i.tar.gz
		outfile=copyEOSProcessed.txt
		echo -e "$(date): processing $i" >> $outfile
		pushd $src
		tar -czf ~/$tarfile $i
		popd
		/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select cp $tarfile $dest
		rm $tarfile
		echo -e "$(date): processed $i" >> $outfile
	fi
done
