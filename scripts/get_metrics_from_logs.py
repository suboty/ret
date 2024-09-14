import os
import re
import argparse
import datetime
import statistics
from pathlib import Path


# python3 get_metrics_from_logs.py -p "../result_de.log" -n de


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for get metrics from logs')
    parser.add_argument('-p', '--path', type=str, help='Path to logs')
    parser.add_argument('-n', '--name', type=str, help='Algorithm`s name')
    args = parser.parse_args()

    name = args.name
    path = args.path

    regex_for_find = re.compile(r'(?<=Current\sbest:\s)[\d.]*')

    print(f'Prepare metrics for {name} algorithm...')

    with open(path, 'r') as logs_file:
        data = logs_file.readlines()

    target_function_values = []
    for row in data:
        _res = regex_for_find.search(row)
        if _res:
            target_function_values.append(float(_res.group(0)))

    _mean = round(statistics.mean(target_function_values), 6)
    _stdev = round(statistics.stdev(target_function_values), 6)
    _median = round(statistics.median(target_function_values), 6)
    _cv = round(statistics.stdev(target_function_values) / statistics.mean(target_function_values), 3)

    path_to_result = Path(
        '..',
        name,
        f'metrics_{datetime.datetime.now().strftime("%d_%m_%y_%I_%M_%s")}'
    )

    os.makedirs(path_to_result, exist_ok=True)

    with open(Path(path_to_result, 'statistics'), 'w') as statistics_file:
        statistics_file.write(f'mean|{_mean}\n')
        statistics_file.write(f'stdev|{_stdev}\n')
        statistics_file.write(f'median|{_median}\n')
        statistics_file.write(f'cv|{_cv}')

    with open(Path(path_to_result, 'tf_values'), 'w') as tf_value_file:
        tf_value_file.writelines([str(x)+'\n' for x in target_function_values])

    print(f'Metrics for {name} algorithm is ready')
