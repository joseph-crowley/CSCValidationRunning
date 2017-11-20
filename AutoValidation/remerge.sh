runDir=${1:-/eos/cms/store/group/dpg_csc/comm_csc/cscval/www/results}
batchDir=${2:-/eos/cms/store/group/dpg_csc/comm_csc/cscval/batch_output}

declare -a datasets=(ExpressPhysics DoubleMuon SingleMuon Cosmics)
# declare -a datasets=(SingleMuon)
declare -a datasets=(SingleMuon DoubleMuon)
for ds in ${datasets[@]}; do
    for i in $(ls "$ds"); do
        [[ ! ${i:0:3} == "run" ]] && continue
        [[ ${i:4:6} -lt 306000 ]] && continue
        [[ ${i:4:6} -gt 307000 ]] && continue
        j="run${i:4:6}"
        # testfile="$runDir/$j/$ds/Site/PNGS/Efficiency_hSEff.png"
        # testfile="$runDir/$j/$ds/Site/PNGS/timeChamberByType-42.png"
        # testfile="$runDir/$j/$ds/Site/PNGS/Sglobal_station_+2.png"
        # testfile="$runDir/$j/$ds/Site/PNGS/cscLCTOccupancy.png"
        # if [ ! -f $testfile ]; then
        [[ ! -d $runDir/$j/$ds/Site/ ]] && continue
        nPlots=`ls -l $runDir/$j/$ds/Site/PNGS/ | wc -l`
        # echo Checked $runDir/$j/$ds/Site/PNGS/ , has $nPlots
        if [[ $nPlots -lt 400 ]]; then
            # echo rm -r $ds/$i
            # echo rm -r $batchDir/$ds/${j}_RAW
            # rm -r $ds/$i
            # rm -r $batchDir/$ds/${j}_RAW
            [ -f $ds/$i/out.txt ] || continue
            njob=`cat $ds/$i/out.txt`
            [[ $njob == "job_0" ]] || [[ $njob == "" ]] && continue
            echo To redo $ds/$i, has $nPlots plots
            # cat $ds/$i/out.txt
            echo "job_0" > $ds/$i/out.txt
        # else
            # echo Run $ds/$i is finished, removing all config files 
            # rm -r $ds/$i LSFJOB* *_cfg.py
        fi
    done
done

# declare -a datasets=(DoubleMuon)
declare -a datasets=(DoubleMuon SingleMuon)
for ds in ${datasets[@]}; do
    for i in $(ls "$ds"); do
        [[ ! ${i:0:3} == "run" ]] && continue
        j="run${i:4:6}_RAW"
        auxfile="$batchDir/$ds/$j/core.*"
        if auxfile=`ls $auxfile 2> /dev/null` ; then
            echo rm $j/core.*
            rm $auxfile
            # echo $ds/$i/out.txt
            # cat $ds/$i/out.txt
            # echo "job_0" > $ds/$i/out.txt
        fi
    done
done            
