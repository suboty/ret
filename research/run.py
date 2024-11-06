import re
import time
import random

from coevolutionary.utils import Utils
from coevolutionary.utils import regex_process
from coevolutionary.utils.terminals import get_terminals
from coevolutionary.manager import CompetitiveManager
from coevolutionary.metrics import Metrics
from coevolutionary.algorithms.gep import GEPAlgorithm
from coevolutionary.utils.tests import check_wilcoxon


INPUT_REGEX = '((((a|bb?)|(a|ba?)|([0-9]|.ab))|(cd|dc|ce|de).ab)|(dc))?abc'


def get_init_data():
    input_regex = INPUT_REGEX

    _params = {
        'range': ['0-9'],
        'repeat': ['0,1'],
    }

    _nodes = {
        # functions (except any)
        -1: 'params',
        0: 'seq',
        1: 'atom',
        2: 'any',
        3: 'repeat',
        4: 'alt',
        5: 'altgroup',
        6: 'group',
        7: 'range',
        8: 'escape',

        # terminals (get by input regex)
        9: 'a',
        10: 'b',
        11: 'c',
        12: 'd',
        13: 'e'
    }

    test_strings = Utils.get_test_strings(
        input_regex=input_regex,
        n_fuzzy_strings=5
    )

    init_metric = Metrics.get_performance_metric(
        regex=re.compile(input_regex),
        test_strings=test_strings,
        n_iter=100,
    )

    _X, _Y = Utils.create_training_set(
        test_strings=test_strings,
        original_regex=input_regex,
        process_func=regex_process,
    )

    _terminals = get_terminals(
        add_digits=False,
        add_lower_latin_letters=False,
        add_custom_symbols=True,
        custom_symbols=['a', 'b', 'c', 'd', 'any', 'range', 'escape']
    )

    return init_metric, _params, _nodes, _X, _Y, _terminals


def add_alg(manager, name, case, alg_object):
    manager.add_algorithm(
        name=name,
        init_params=case,
        init_algorithm=alg_object.init_algorithm,
        init_population=alg_object.init_population,
        get_fitness_population=alg_object.get_fitness_population,
        select_population=alg_object.select_population,
        recombine_population=alg_object.recombine_population,
        mutate_population=alg_object.mutate_population,
    )
    return manager


if __name__ == '__main__':
    random.seed(456)

    INIT_METRIC, params, nodes, X, Y, terminals = get_init_data()

    gep_params_cases = [
        {'population_length': 10, 'genes_n': 3, 'head_n': 2, 'n_elites': 1},
    ]

    cm_manager_params = [
        {'shared_resource': 400, 'social_card': 0.2, 'penalty': 0.1, 'adaptive_interval': 5},
    ]

    numbers_of_individual_alg = [3, 4, 5, 6]
    exp_counter = 0

    for number_of_individual_alg in numbers_of_individual_alg:
        for _ in range(20):
            for m_i, manager_case in enumerate(cm_manager_params):
                print(f'### CM MANAGER PARAMS {m_i}')
                exp_name = f'exp_{round(time.time())}'

                print('### GEP ###')
                print('\nCOEVOLUTION\n')
                # coevolution
                cm = CompetitiveManager(
                    adaptive_interval=manager_case['adaptive_interval'],
                    shared_resource=manager_case['shared_resource'],
                    verbose=False,
                    problem='min',
                    survive_schema='best',
                    social_card=manager_case['social_card'],
                    penalty=manager_case['penalty'],
                    experiment_name=str(exp_counter),
                    input_regex=INPUT_REGEX,
                    input_metric=INIT_METRIC
                )

                for i, _ in enumerate(range(number_of_individual_alg)):
                    gep_object = GEPAlgorithm(X=X, Y=Y, n_iter=100, terminals=terminals, params=params, )
                    cm = add_alg(
                        manager=cm,
                        name=f'gep_{i}_coev',
                        case=gep_params_cases[0],
                        alg_object=gep_object
                    )
                cm.run_coevolution()

                coevolution_algorithm_history = cm.algorithm_history
                population_qualities_history = cm.population_qualities_history
                coev_names = cm.get_algorithm_names()
                best_alg_statistics = cm.get_winner_statistics()

                cm.save_algorithms_qualities()

                # separately
                print('\nSEPARATELY\n')
                separately_algorithm_history = {}
                sep_names = []

                for i, _ in enumerate(range(number_of_individual_alg)):
                    cm = CompetitiveManager(
                        adaptive_interval=manager_case['adaptive_interval'],
                        shared_resource=manager_case['shared_resource'],
                        verbose=False,
                        problem='min',
                        survive_schema='best',
                        social_card=manager_case['social_card'],
                        penalty=manager_case['penalty'],
                        experiment_name=str(exp_counter),
                        input_regex=INPUT_REGEX,
                        input_metric=INIT_METRIC
                    )

                    gep_object = GEPAlgorithm(X=X, Y=Y, n_iter=100, terminals=terminals, params=params, )

                    cm = add_alg(
                        manager=cm,
                        name=f'gep_{i}_sep',
                        case=gep_params_cases[0],
                        alg_object=gep_object
                    )

                    # overload run
                    cm.run_coevolution()

                    separately_algorithm_history[i] = cm.algorithm_history[0]
                    sep_names.append(f'gep_{i}_sep')

                    check_wilcoxon(
                        history_a=cm.algorithm_history,
                        history_b=best_alg_statistics,
                        a_name=f'gep_{i}_sep',
                        b_name=f'best of coevolutionary gep',
                        a_index=0,
                        b_index=i,
                        metric_number=1,
                        metric_name='minimum'
                    )

        exp_counter += 1
