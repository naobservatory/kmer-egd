#!/usr/bin/env bash

head -n 1 clean-HTP-spike-contigs.* | \
    grep . | \
    sed s/==// | \
    sed 's/ <==//' | \
    sed -E 's/^[0-9]*\t//' > \
        all-spike-contigs.fasta

zip -r clean-HTP.zip all-spike-contigs.fasta clean-HTP-spike-*.display

aws s3 cp clean-HTP.zip s3://prjna729801/
