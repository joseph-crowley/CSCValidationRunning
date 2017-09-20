runDir=${1:-/eos/cms/store/group/dpg_csc/comm_csc/cscval/www/results}
batchDir=${2:-/eos/cms/store/group/dpg_csc/comm_csc/cscval/batch_output}

declare -a datasets=(ExpressPhysics DoubleMuon SingleMuon Cosmics)
for ds in ${datasets[@]}; do
    for i in $(ls "$ds"); do
        [[ ! ${i:0:3} == "run" ]] && continue
        j="run${i:4:6}"
         testfile="$runDir/$j/$ds/Site/PNGS/Efficiency_hSEff.png"
        #testfile="$runDir/$j/$ds/Site/PNGS/timeChamberByType-42.png"
        if [ ! -f $testfile ]; then
            # echo rm -r $ds/$i
            # echo rm -r $batchDir/$ds/${j}_RAW
            # rm -r $ds/$i
            # rm -r $batchDir/$ds/${j}_RAW
            [ -f $ds/$i/out.txt ] || continue
            njob=`cat $ds/$i/out.txt`
            [[ $njob == "job_0" ]] || [[ $njob == "" ]] && continue
            echo $ds/$i/out.txt
            # cat $ds/$i/out.txt
            echo "job_0" > $ds/$i/out.txt
        fi
    done
done            
