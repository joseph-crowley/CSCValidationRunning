for file in *_merge.err; do
    sed -i '/.png has been created/d' $file
done

for file in *_merge.err; do
    sed -i '/R__unzip/d' $file
done

for file in *_merge.err; do
    sed -i '/: No such process/d' $file
done

for file in *_merge.err; do
    sed -i '/<TBasket::ReadBasketBuffers>/d' $file
done
