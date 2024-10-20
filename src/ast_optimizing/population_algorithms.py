import copy
import os
import re
import datetime
from pathlib import Path

from mealpy import FloatVar, DE, PSO, SHADE

from src.logger import logger
from src.generating.matrix import GeneratorByIncidence
from src.metrics.performance import get_performance_metric
from src.metrics.accuracy import get_match_accuracy

INCIDENCE_LIST_COFF = 1
INCIDENCE_LIST_LEN = 0
MAX_SOLUTION_VALUE = 0
N_ITER_FOR_PERFORMANCE = 100
PHRASES = []
SEED = 456

# TODO: add syntax choice


def _regex_generator(*args):
    return args


_params = None
_nodes = None


def validate_regex_compiling(regex):
    try:
        _ = re.compile(regex)
    except:
        raise AttributeError


def get_solution_metric(solution, phrases):

    # get regex by solution
    try:
        regex = _regex_generator(solution, copy.deepcopy(_params), _nodes)
        validate_regex_compiling(regex)
    except:
        raise AttributeError('Error while regex generating')

    # count accuracy
    accuracy = []
    for phrase in phrases:
        _acc_res = get_match_accuracy(
            regex=regex,
            syntax=1,
            phrase=phrase
        )
        accuracy.append(_acc_res)

    coeff = (2. - sum(accuracy)/len(accuracy))

    # count performance metric
    res_metric =  coeff * float(get_performance_metric(
            regex=regex,
            syntax=1,
            n_iter=N_ITER_FOR_PERFORMANCE,
    ))

    return res_metric


def objective_function(solution):
    solution = solution.round().reshape((INCIDENCE_LIST_LEN * INCIDENCE_LIST_COFF, 2))

    try:
        return get_solution_metric(solution, PHRASES)
    except:
        return MAX_SOLUTION_VALUE * 2


class PopulationAlgorithmsOptimizing:
    # TODO: refactor class structure

    allowed_algorithms = [
        'de', 'differential evolution',
        'pso', 'particle swarm optimization',
        'shade', 'success history adaptation differential evolution'
    ]

    algorithms_params = {
        'DE': {
            "bounds": FloatVar(),
            "minmax": "min",
            "obj_func": objective_function,
            "epoch": 100,
            "pop_size": 100,
        },
        'PSO': {
            "bounds": FloatVar(),
            "minmax": "min",
            "obj_func": objective_function,
            "epoch": 100,
            "pop_size": 100,
            "c1": 2.05,
            "c2": 2.05,
            "alpha": 0.4
        },
        'SHADE': {
            "bounds": FloatVar(),
            "minmax": "min",
            "obj_func": objective_function,
            "epoch": 100,
            "pop_size": 100,
            "miu_f": 0.5,
            "miu_cr": 0.5
        }
    }

    regex_generator = GeneratorByIncidence()
    last_tf_value = None
    max_solution_value = None

    def __init__(self):
        os.makedirs('logs', exist_ok=True)

    def get_optimizing_matrix_by_de(self):

        problem_dict = {
            "bounds": self.algorithms_params.get('DE').get('bounds'),
            "minmax": self.algorithms_params.get('DE').get('minmax'),
            "obj_func": objective_function,
            "log_to": "file",
            "log_file": str(Path(
                'logs',
                f'result_de_{datetime.datetime.now().strftime("%d_%m_%y_%I_%M_%s")}.log'
            ))
        }

        model = DE.SADE(
            epoch=self.algorithms_params.get('DE').get('epoch'),
            pop_size=self.algorithms_params.get('DE').get('pop_size')
        )
        g_best = model.solve(problem_dict, seed=SEED)

        return g_best.solution

    def get_optimizing_matrix_by_shade(self):

        problem_dict = {
            "bounds": self.algorithms_params.get('SHADE').get('bounds'),
            "minmax": self.algorithms_params.get('SHADE').get('minmax'),
            "obj_func": objective_function,
            "log_to": "file",
            "log_file": str(Path(
                'logs',
                f'result_shade_{datetime.datetime.now().strftime("%d_%m_%y_%I_%M_%s")}.log'
            ))
        }

        model = SHADE.L_SHADE(
            epoch=self.algorithms_params.get('SHADE').get('epoch'),
            pop_size=self.algorithms_params.get('SHADE').get('pop_size'),
            miu_f=self.algorithms_params.get('SHADE').get('miu_f'),
            miu_cr=self.algorithms_params.get('SHADE').get('miu_cr')
        )
        g_best = model.solve(problem_dict, seed=SEED)

        return g_best.solution

    def get_optimizing_matrix_by_pso(self):

        problem_dict = {
            "bounds": self.algorithms_params.get('PSO').get('bounds'),
            "minmax": self.algorithms_params.get('PSO').get('minmax'),
            "obj_func": objective_function,
            "log_to": "file",
            "log_file": str(Path(
                'logs',
                f'result_pso_{datetime.datetime.now().strftime("%d_%m_%y_%I_%M_%s")}.log'
            ))
        }

        model = PSO.AIW_PSO(
            epoch=self.algorithms_params.get('PSO').get('epoch'),
            pop_size=self.algorithms_params.get('PSO').get('pop_size'),
            c1=self.algorithms_params.get('PSO').get('c1'),
            c2=self.algorithms_params.get('PSO').get('c2'),
            alpha=self.algorithms_params.get('PSO').get('alpha')
        )
        g_best = model.solve(problem_dict, seed=SEED)

        return g_best.solution

    def __call__(self, incidence_list, params, nodes, algorithm, phrases):
        if algorithm.lower() not in self.allowed_algorithms:
            raise NotImplementedError(f'Optimizing by algorithm {algorithm} is not implemented')

        optim_incidence_list = None

        global INCIDENCE_LIST_LEN, PHRASES, MAX_SOLUTION_VALUE
        INCIDENCE_LIST_LEN = len(incidence_list)
        PHRASES = phrases

        global _regex_generator, _params, _nodes
        _regex_generator = self.regex_generator
        _params = copy.deepcopy(params)
        _nodes = nodes

        MAX_SOLUTION_VALUE = get_solution_metric(incidence_list, phrases)
        self.max_solution_value = round(MAX_SOLUTION_VALUE, 8)

        max_id = sorted([int(x) for x in nodes.keys()], reverse=True)[0]

        # TODO: fix params settings
        self.algorithms_params['DE']['bounds'] = FloatVar(
            lb=(0,) * len(incidence_list) * 2 * INCIDENCE_LIST_COFF,
            ub=(max_id,) * len(incidence_list) * 2 * INCIDENCE_LIST_COFF,
            name="delta"
        )
        self.algorithms_params['PSO']['bounds'] = self.algorithms_params['DE']['bounds']
        self.algorithms_params['SHADE']['bounds'] = self.algorithms_params['DE']['bounds']

        try:
            match algorithm:
                case 'pso' | 'particle swarm optimization':
                    optim_incidence_list = self.get_optimizing_matrix_by_pso()
                case 'de' | 'differential evolution':
                    optim_incidence_list = self.get_optimizing_matrix_by_de()
                case 'shade' | 'success history adaptation differential evolution':
                    optim_incidence_list = self.get_optimizing_matrix_by_shade()

            optim_incidence_list = optim_incidence_list.round().reshape(
                (
                    INCIDENCE_LIST_LEN * INCIDENCE_LIST_COFF,
                    2
                )
            )

            self.last_tf_value = round(objective_function(optim_incidence_list), 8)

            return optim_incidence_list
        except Exception as e:
            logger.error(
                message='Error while regex optimizing',
                exc=e,
            )
            return incidence_list
