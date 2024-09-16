import os
import statistics
import argparse
from pathlib import Path

from utils import create_algorithm_boxplot, create_algorithm_plot

names_rus_mapping = {
    'de': 'ДЭ',
    'pso': 'РЧ'
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for get plots from metrics')
    parser.add_argument('-p', '--path', type=str, default='metrics', help='Path to metrics')
    parser.add_argument('-n', '--name', type=str, help='Algorithm`s name')
    args = parser.parse_args()

    name = args.name
    path = args.path

    os.makedirs('plots', exist_ok=True)

    print(f'Prepare plots for {name} algorithm...')

    os.chdir(path)
    metrics_list = [x for x in os.listdir()
                 if name in x]
    os.chdir('..')

    metrics = []

    for metric_path in metrics_list:
        with open(Path(path, metric_path), 'r') as metric_file:
            metrics.append(
                [float(x.replace('\n', '')) for x in metric_file.readlines()]
            )

    best_metric = metrics[0]
    _metrics = metrics[0]

    for metric in metrics[1:]:
        mean_best_metrics = statistics.mean(best_metric)
        mean_current_metrics = statistics.mean(metric)

        if mean_current_metrics < mean_best_metrics:
            best_metric = metric

        _metrics += metric

    create_algorithm_boxplot(
        data=_metrics,
        name=names_rus_mapping[name],
    )

    create_algorithm_plot(
        data=best_metric,
        name=names_rus_mapping[name],
    )

    print(f'Plots for {name} algorithm is ready')
