for a in A C G T; do
  for b in A C G T; do
    aws s3 cp s3://prjna729801/hc-HTP-$a$b.gz - |\
      gunzip | \
      perl -ne 'print if (rand() < .01)' | \
      awk '{sum=0; for(i=2;i<=NF;i++) sum+=$i; if(sum>10) print}' | \
      awk '{days=0; for(i=2;i<=NF;i++) if($i>0) days+=1; if(days>3) print}' > \
          HTP-$a$b.gt10c.gt3d &
    done
done
wait
cat HTP-*.gt10c.gt3d | sort | tr '\t' ',' > HTP.gt10c.gt3d.csv
