# Usage: ./find-subsetted-kmers.sh sars-cov-2.fasta 40

GENOME_FASTA="$1"
HASH_DENOM="$2"

GREP_TARGET=$(cat "${GENOME_FASTA}" | \
    python3 to-kmers.py "$HASH_DENOM" | \
    sort | \
    tr '\n' '|' | \
    sed 's/.$//' | \
    sed 's~|~\\|~g')

cat rothman.unenriched_samples | \
    awk '{print $1}' | \
    xargs -P 32 -I {} bash -c "aws s3 cp s3://prjna729801/{} - | \
      gunzip | \
      grep -B 1 --no-group-separator '${GREP_TARGET}' > \
      {}.$HASH_DENOM.covid_matches.fasta"
