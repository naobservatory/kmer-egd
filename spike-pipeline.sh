# Given raw reads:
# 1. Count how many times each k-mer appears on each day
# 2. Identify k-mers that appear almost entirely on a single
#    day ("spiking k-mers").
# 3. Assemble those k-mers into contigs ("spike contigs")
# 4. For each spike contig:
#    a. Find all matching reads
#    b. Align those reads to the contig
#    c. Display them, with mismatching bases highlighted

echo "Trimming adapters..."
./trim-adapters.sh
echo "Counting kmers..."
./count-wtp.sh
echo "Finding spikes..."
./find-all-spikes.sh
echo "Splitting spikes by day..."
./partition-spikes.sh
echo "Assembling spike contigs for each day..."
./assemble-spike-contigs.sh
echo "Finding matching reads..."
./extract-spike-reads.sh
echo "Aligning reads back to contigs"
./align-reads-to-contigs.sh
echo "Preparing for display..."
./display-all-reads.sh
