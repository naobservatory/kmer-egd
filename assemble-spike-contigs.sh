for day in {00..20} ; do
    prefix=hc-HTP-spike-contigs.$day
    if ls $prefix.* &> /dev/null; then
        continue
    fi
    
    fname_in="s3://prjna729801/hc-HTP.spikes.$day.gz"
    aws s3 cp $fname_in - | \
        gunzip | \
        awk '$1>300{print}' | \
        python3 assemble.py $prefix
done
