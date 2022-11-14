for day in {00..20}; do
    prefix=hc-HTP-spike-reads.$day.c
    if ls $prefix.* &> /dev/null; then
        continue
    fi

    for one in hc-HTP-spike-reads.$day.1.* ; do
        cat $one ${one/.$day.1./.$day.2.} > ${one/.$day.1./.$day.c.}
        rm $one
        rm ${one/.$day.1./.$day.2.}
    done
done
