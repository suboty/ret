import sys
import subprocess
from pathlib import Path
from typing import List

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
    import matplotlib.pyplot as plt


plt.rcParams['figure.autolayout'] = True


def create_algorithm_plot(
        data: List,
        name: str,
        n_iter: int = 100
):
    plt.title(name)
    plt.plot(data, color='black')
    plt.grid(True)
    ax = plt.gca()

    ax.set_ylabel("Значение целевой функции, мс", fontsize=12, color='black')  # +
    ax.set_xlabel("Поколения", fontsize=12, color='black')  # +

    plt.scatter([n_iter], data[-1], color='red')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    plt.savefig(Path('plots', f"plot_{name}.png"))
    plt.clf()


def create_algorithm_boxplot(name: str, data: List):
    plt.title(name)
    plt.boxplot(data)
    plt.grid(True)
    bax = plt.gca()

    bax.set_ylabel("Значение целевой функции, мс", fontsize=12, color='black')

    bax.xaxis.set_ticks_position('bottom')
    bax.yaxis.set_ticks_position('left')

    plt.savefig(Path('plots', f"boxplot_{name}.png"))
    plt.clf()
