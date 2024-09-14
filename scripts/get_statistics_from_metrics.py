import os
import re
import argparse
import datetime
import statistics
from pathlib import Path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for get statistics from metrics')
    parser.add_argument('-p', '--path', type=str, default='metrics', help='Path to tf values')
    parser.add_argument('-n', '--name', type=str, help='Algorithm`s name')
    args = parser.parse_args()

    name = args.name
    path = args.path

    os.makedirs('statistics', exist_ok=True)

    print(f'Prepare statistics for {name} algorithm...')

    os.chdir(path)
    values_lists = [x for x in os.listdir()
                    if name in x]
    os.chdir('..')

    if len(values_lists) == 0:
        raise AttributeError(f'Error! No files for <{name}> algorithm.')

    tf_values = []

    for values_list_path in values_lists:
        with open(Path(path, values_list_path), 'r') as tf_value_list:
            data = [float(x.replace('\n', '')) for x in tf_value_list.readlines()]
            tf_values += data

    _mean = round(statistics.mean(tf_values), 6)
    _stdev = round(statistics.stdev(tf_values), 6)
    _median = round(statistics.median(tf_values), 6)
    _cv = round(statistics.stdev(tf_values) / statistics.mean(tf_values), 3)

    with open(Path('statistics', f'{name}.statistics'), 'w') as statistics_file:
        statistics_file.write(f'mean|{_mean:.6f}\n')
        statistics_file.write(f'stdev|{_stdev:.6f}\n')
        statistics_file.write(f'median|{_median:.6f}\n')
        statistics_file.write(f'cv|{_cv:.6f}')

    print(f'Statistics for {name} algorithm is ready')
