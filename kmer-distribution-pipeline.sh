echo "Determining what inputs to consider..."
./find-best-timeseries.sh
echo "Trimming adapters..."
./trim-consistent-timeseries.sh
echo "Counting kmers..."
./count-consistent-timeseries.sh
