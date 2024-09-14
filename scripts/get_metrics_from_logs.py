import os
import re
import argparse
import datetime
from pathlib import Path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for get metrics from logs')
    parser.add_argument('-p', '--path', type=str, default='logs', help='Path to logs')
    parser.add_argument('-n', '--name', type=str, help='Algorithm`s name')
    args = parser.parse_args()

    name = args.name
    path = args.path

    os.makedirs('metrics', exist_ok=True)

    regex_for_find = re.compile(r'(?<=Current\sbest:\s)[\d.\-e]*')

    print(f'Prepare metrics for {name} algorithm...')

    os.chdir(path)
    logs_list = [x for x in os.listdir()
                 if name in x]
    os.chdir('..')

    for log_file_path in logs_list:

        _date = log_file_path.replace(f'result_{name}_', '').replace('.log', '')

        with open(Path(path, log_file_path), 'r') as logs_file:
            data = logs_file.readlines()

        target_function_values = []
        for row in data:
            _res = regex_for_find.search(row)
            if _res:
                value = round(float(_res.group(0)), 6)
                target_function_values.append(f'{value:.6f}')

        with open(
                Path(
                    'metrics',
                    f'{name}_tf_values_{_date}.metrics'),
                'w') as tf_value_file:
            tf_value_file.writelines([str(x)+'\n' for x in target_function_values])

    print(f'Metrics for {name} algorithm is ready')
