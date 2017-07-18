for file in *_merge.err; do
    sed -i '/.png has been created/d' $file
done
