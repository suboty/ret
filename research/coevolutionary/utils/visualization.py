import random
from typing import Dict, List

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (15, 10)

_statistics_dict = {
    0: 'len',
    1: 'min',
    2: 'max',
    3: 'mean',
    4: 'stdev',
    5: 'median',
    6: 'cv',
    7: 'invalid numbers'
}

line_styles = [
    'solid',
    'dotted',
    'dashed',
    'dashdot'
]


def preprocess_history(history):
    new_history = [history[0]]

    max_v = max(history)
    min_v = min(history)

    for i, entry in enumerate(history[1:]):
        if int(entry) == 1:
            new_history.append(
                (history[i - 1] - min_v) / (max_v - min_v)
            )
        else:
            new_history.append(
                (entry - min_v) / (max_v - min_v)
            )
    return new_history


def log_history(history):
    return np.log(np.array(history) + 1)


def visualize(
        algorithm_history: Dict,
        algorithm_names: List
):
    fig, axs = plt.subplots(2, 3)

    alg_dict = {}

    for i, key in enumerate(algorithm_history.keys()):
        for j, row in enumerate(algorithm_history[key]):
            if j == 0:
                alg_dict[i] = {}
                alg_dict[i][0] = [row[0]]
                alg_dict[i][1] = [row[1]]
                alg_dict[i][2] = [row[2]]
                alg_dict[i][3] = [row[3]]
                alg_dict[i][4] = [row[7]]
                alg_dict[i][5] = [row[6]]
            else:
                alg_dict[i][0].append(row[0])
                alg_dict[i][1].append(row[1])
                alg_dict[i][2].append(row[2])
                alg_dict[i][3].append(row[3])
                alg_dict[i][4].append(row[7])
                alg_dict[i][5].append(row[6])

    for i in alg_dict.keys():
        axs[0, 0].plot(alg_dict[i][0], label=algorithm_names[i], linestyle=random.choice(line_styles))
        axs[1, 0].plot(alg_dict[i][1], label=algorithm_names[i], linestyle=random.choice(line_styles))
        axs[0, 1].plot(alg_dict[i][2], label=algorithm_names[i], linestyle=random.choice(line_styles))
        axs[1, 1].plot(alg_dict[i][3], label=algorithm_names[i], linestyle=random.choice(line_styles))
        axs[0, 2].plot(alg_dict[i][4], label=algorithm_names[i], linestyle=random.choice(line_styles))
        axs[1, 2].plot(alg_dict[i][5], label=algorithm_names[i], linestyle=random.choice(line_styles))

    axs[0, 0].set_title(_statistics_dict[0])
    axs[0, 0].legend(loc="best")
    axs[0, 0].set_xlabel('algorithm iterations')
    axs[0, 0].set_ylabel('length of population')

    axs[1, 0].set_title(_statistics_dict[1])
    axs[1, 0].legend(loc="best")
    axs[1, 0].set_xlabel('algorithm iterations')
    axs[1, 0].set_ylabel('minimum value of metric in population')

    axs[0, 1].set_title(_statistics_dict[2])
    axs[0, 1].legend(loc="best")
    axs[0, 1].set_xlabel('algorithm iterations')
    axs[0, 1].set_ylabel('maximum value of metric in population')

    axs[1, 1].set_title(_statistics_dict[3])
    axs[1, 1].legend(loc="best")
    axs[1, 1].set_xlabel('algorithm iterations')
    axs[1, 1].set_ylabel('average value of metric in population')

    axs[0, 2].set_title(_statistics_dict[7])
    axs[0, 2].legend(loc="best")
    axs[0, 2].set_xlabel('algorithm iterations')
    axs[0, 2].set_ylabel('invalid individuals in population')

    axs[1, 2].set_title(_statistics_dict[6])
    axs[1, 2].legend(loc="best")
    axs[1, 2].set_xlabel('algorithm iterations')
    axs[1, 2].set_ylabel('coefficient of variation of metric values in population')

    plt.tight_layout()
    plt.show()


def visualize_algorithms_quality(
    population_qualities_history: List,
    algorithm_names: List
):
    plt.title('algorithm qualities')
    alg_dicts = {}
    for i, row in enumerate(population_qualities_history):
        if i == 0:
            for j, alg in enumerate(row):
                alg_dicts[j] = [row[j]]
        else:
            for j, alg in enumerate(row):
                alg_dicts[j].append(row[j])

    for i, alg in enumerate(algorithm_names):
        plt.plot(
            log_history(
                alg_dicts[i]
            ),
            label=alg,
            linestyle = random.choice(line_styles)
        )
    plt.legend(loc="best")
    plt.xlabel("algorithm iterations")
    plt.ylabel("algorithm quality")
    plt.grid()
    plt.show()
