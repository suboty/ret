#!/bin/bash

echo "start for <$1> ..."
rm -r metrics
rm -r logs
rm -r statistics
for ((i=1; i < 10; i++))
do
python3 main.py -r $1
done
## de
python3 scripts/get_metrics_from_logs.py -n de
python3 scripts/get_statistics_from_metrics.py -n de
## pso
python3 scripts/get_metrics_from_logs.py -n pso
python3 scripts/get_statistics_from_metrics.py -n pso
echo "end for <$1> ..."
