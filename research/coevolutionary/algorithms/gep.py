import random
from typing import List, Dict

import geppy
from deap import creator, base, tools

import deap
from coevolutionary.metrics import Metrics
from coevolutionary.manager import STUB_VALUE
from coevolutionary.utils.translators import ETtoRegexTranslator


# dummy functions for naming while GEP algorithm works
def alt(*args):
    return args


def group(*args):
    return args


def repeat(*args):
    return args


_functions = {
    alt: 2,
    group: 10,
    repeat: 1,
}


def _apply_modification(population, operator, pb):
    for i in range(len(population)):
        if random.random() < pb:
            population[i], = operator(population[i])
            del population[i].fitness.values
    return population


def _apply_crossover(population, operator, pb):
    for i in range(1, len(population), 2):
        if random.random() < pb:
            population[i - 1], population[i] = operator(population[i - 1], population[i])
            del population[i - 1].fitness.values
            del population[i].fitness.values
    return population


def gep_evaluate(
    individual,
    X: List,
    Y: List,
    n_iter: int,
    terminals: List,
    params: Dict,
):
    res = ETtoRegexTranslator.regex_compile(
        individual=individual,
        terminals=terminals,
        params=params,
    )
    if not res[0]:
        try:
            individual = '(' + individual
            res = ETtoRegexTranslator.regex_compile(
                individual=individual,
                terminals=terminals,
                params=params,
            )
        except:
            return STUB_VALUE,

    regex = res[0]
    # count accuracy metric
    accuracy = []
    for x, y in zip(X, Y):
        accuracy.append(
            Metrics.get_match_accuracy(
                regex=regex,
                phrase=x,
                result=y
            )
        )
    try:
        accuracy = sum(accuracy) / len(accuracy)
        res_metric = (2 - accuracy) * float(
            Metrics.get_performance_metric(
                regex=regex,
                n_iter=n_iter,
                test_strings=X
            ))
    except ZeroDivisionError:
        res_metric = STUB_VALUE

    return res_metric,


class GEPAlgorithm:
    def __init__(
            self,
            X: List,
            Y: List,
            terminals: List,
            params: Dict,
            n_iter: int,
    ):

        # gep params
        self.terminals = terminals
        self.params = params
        self.n_iter = n_iter
        self.head_n = None
        self.genes_n = None
        self.n_elites = None

        # gep inner storages
        self.creator = None
        self.population = None
        self.toolbox = None
        self.init_params = None
        self.elites = None
        self.offspring = None
        self.pset = self.create_primitives_set()

        # X and Y for test dataset
        self.X = X
        self.Y = Y

    def create_primitives_set(self):
        # terminals
        pset = geppy.PrimitiveSet('Main', input_names=self.terminals)

        # functions
        for function in _functions.keys():
            pset.add_function(function, _functions.get(function))
        return pset

    def set_genetic_operators(self):
        toolbox = geppy.Toolbox()
        toolbox.register('select', tools.selRoulette)
        toolbox.register(
            'mut_uniform',
            geppy.mutate_uniform,
            pset=self.pset,
            ind_pb=2 / (2 * self.head_n + 1)
        )
        toolbox.pbs['mut_uniform'] = 0.2
        toolbox.register('mut_invert', geppy.invert, pb=0.1)
        toolbox.register('mut_is_ts', geppy.is_transpose, pb=0.1)
        toolbox.register('mut_ris_ts', geppy.ris_transpose, pb=0.1)
        toolbox.register('mut_gene_ts', geppy.gene_transpose, pb=0.3)
        toolbox.register('cx_1p', geppy.crossover_one_point, pb=0.3)
        toolbox.pbs['cx_1p'] = 0.4
        toolbox.register('cx_2p', geppy.crossover_two_point, pb=0.2)
        toolbox.register('cx_gene', geppy.crossover_gene, pb=0.1)

        return toolbox

    @staticmethod
    def create_individual():
        # to minimize the objective (fitness)
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", geppy.Chromosome, fitness=creator.FitnessMin)
        return creator

    def set_evaluate_function(self, toolbox):
        toolbox.register(
            'evaluate',
            gep_evaluate,
            X=self.X,
            Y=self.Y,
            terminals=self.terminals,
            params=self.params,
        )
        return toolbox

    def create_population(self, toolbox, n):
        toolbox.register(
            'gene_gen',
            geppy.Gene,
            pset=self.pset,
            head_length=self.head_n
        )
        toolbox.register(
            'individual',
            creator.Individual,
            gene_gen=toolbox.gene_gen,
            n_genes=self.genes_n,
            linker=group
        )
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register('compile', geppy.compile_, pset=self.pset)
        pop = toolbox.population(n=n)
        return pop

    def init_algorithm(self, init_params: Dict):
        """Init GEP algorithm"""
        self.init_params = init_params

        self.genes_n = init_params['genes_n']
        self.head_n = init_params['head_n']
        self.n_elites = init_params['n_elites']

        creator = self.create_individual()
        toolbox = self.set_genetic_operators()
        population = self.create_population(
            toolbox, n=init_params['population_length']
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
                n_iter=self.n_iter,
                terminals=self.terminals,
                params=self.params,
            )
            ind.fitness.values = fit
        return self.population

    def select_population(self):
        """Select operators in mutate method"""
        elites = deap.tools.selBest(
            self.population,
            k=self.n_elites)
        offspring = self.toolbox.select(
            self.population,
            len(self.population) - self.n_elites
        )
        offspring = [self.toolbox.clone(ind) for ind in offspring]

        self.elites = elites
        self.offspring = offspring

    def recombine_population(self):
        """Crossover operators in mutate method"""
        self.population = sorted(
            self.population,
            key=lambda x: x.fitness.values[0]
        )

    def mutate_population(self):
        """Mutate operators for GEP population"""
        for op in self.toolbox.pbs:
            if op.startswith('mut'):
                self.offspring = _apply_modification(
                    self.offspring,
                    getattr(self.toolbox, op),
                    self.toolbox.pbs[op]
                )
        # crossover
        for op in self.toolbox.pbs:
            if op.startswith('cx'):
                self.offspring = _apply_crossover(
                    self.offspring,
                    getattr(self.toolbox, op),
                    self.toolbox.pbs[op]
                )
        # replace the current population with the offsprings
        self.population = self.elites + self.offspring

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
                n_iter=self.n_iter,
                terminals=self.terminals,
                params=self.params,
            )
            fitnesses.append(individual.fitness.values)
        return fitnesses