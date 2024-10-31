import re
import array
import random
from typing import Dict, List

import numpy as np
from deap import creator, base, tools

from coevolutionary.manager import STUB_VALUE
from coevolutionary.metrics import Metrics
from coevolutionary.utils.translators import ILtoRegexTranslator

import os

os.chdir('..')
from src.metrics.readability import get_readability
os.chdir('research')

# 1 - performance
# 2 - readability
__SCHEMA = 1


def de_evaluate(
        individual,
        X: List,
        Y: List,
        translator: ILtoRegexTranslator,
        n_iter: int
):
    if not isinstance(individual, List):
        individual = individual.tolist()

    individual = np.array(
        [abs(x) for x in individual]
    ).round().reshape((-1, 2))

    if __SCHEMA == 1:
        res = translator.regex_compile(individual)
        if not res[0]:
            return STUB_VALUE,
        regex = re.compile(res[0])
    else:
        res = translator.regex_compile(individual, is_need_string=True)
        regex = res[0]
        if not regex:
            return STUB_VALUE,

    # count accuracy metric
    accuracy = []
    for x, y in zip(X, Y):
        accuracy.append(
            Metrics.get_match_accuracy(
                regex=regex if __SCHEMA == 2 else re.compile(regex),
                phrase=x,
                result=y
            )
        )
    try:
        accuracy = sum(accuracy) / len(accuracy)
        if __SCHEMA == 1:
            res_metric = (2 - accuracy) * float(
                Metrics.get_performance_metric(
                    regex=regex,
                    n_iter=n_iter,
                    test_strings=X
                ))
        else:
            res_metric = (2 - accuracy) * float(
                Metrics.get_readability(
                    regex_string=regex,
                )
            )
    except ZeroDivisionError:
        res_metric = STUB_VALUE
    return res_metric,


class DEAlgorithm:
    def __init__(
            self,
            nodes,
            params,
            X: List,
            Y: List,
            n_iter: int,
    ):

        # de inner storages
        self.creator = None
        self.population = None
        self.toolbox = None
        self.init_params = None

        # de genetic params
        self.__select_number = 3

        self.n_iter = n_iter

        # X and Y for test dataset
        self.X = X
        self.Y = Y

        self.translator = ILtoRegexTranslator(
            nodes=nodes,
            params=params,
        )

    def set_genetic_operators(self):
        toolbox = base.Toolbox()
        toolbox.register(
            "attr_float",
            random.uniform,
            self.init_params['bounds'][0],
            self.init_params['bounds'][1]
        )
        toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            toolbox.attr_float,
            self.init_params['ndim']
        )
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("select", tools.selRandom, k=self.__select_number)
        return toolbox

    @staticmethod
    def create_individual():
        # to minimize the objective (fitness)
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)
        return creator

    def set_evaluate_function(self, toolbox):
        toolbox.register(
            'evaluate',
            de_evaluate,
            X=self.X,
            Y=self.Y,
            translator=self.translator
        )
        return toolbox

    def create_population(self, toolbox, n):
        pop = toolbox.population(n=n)
        return pop

    def init_algorithm(self, init_params: Dict):
        """Init DE algorithm"""
        self.init_params = init_params
        creator = self.create_individual()
        toolbox = self.set_genetic_operators()
        population = self.create_population(
            toolbox, n=init_params['mu']
        )

        toolbox = self.set_evaluate_function(toolbox)

        self.creator = creator
        self.population = population
        self.toolbox = toolbox
        self.init_params = init_params

        return self

    def init_population(self) -> List:
        """Get the zero population"""
        for ind in self.population:
            fit = self.toolbox.evaluate(
                ind,
                X=self.X,
                Y=self.Y,
                n_iter=self.n_iter
            )
            ind.fitness.values = fit
        return self.population

    def select_population(self):
        """Select operators in mutate method"""
        pass

    def recombine_population(self):
        """Crossover operators in mutate method"""
        self.population = sorted(
            self.population,
            key=lambda x: x.fitness.values[0]
        )

    def mutate_population(self):
        """Mutate operators for DE population"""
        for k, agent in enumerate(self.population):
            a, b, c = self.toolbox.select(self.population)
            y = self.toolbox.clone(agent)
            for i, value in enumerate(agent):
                if random.random() < self.init_params['cr']:
                    y[i] = a[i] + self.init_params['f'] * (b[i] - c[i])
            y_fitness = self.toolbox.evaluate(
                y,
                X=self.X,
                Y=self.Y,
                n_iter=self.n_iter
            )
            if y_fitness[0] < agent.fitness.values[0]:
                self.population[k] = agent

    def get_fitness_population(self, is_init_population: bool = False) -> List:
        """Get fitness values for DE population"""
        if is_init_population:
            fitnesses = []
            start_index = 0
        else:
            fitnesses = [self.population[0].fitness.values]
            start_index = 1
        for individual in self.population[start_index:]:
            individual.fitness.values = self.toolbox.evaluate(
                individual,
                X=self.X,
                Y=self.Y,
                n_iter=self.n_iter
            )
            fitnesses.append(individual.fitness.values)
        return fitnesses
