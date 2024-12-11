import re
import random

from coevolutionary.utils import Utils
from coevolutionary.utils import regex_process
from coevolutionary.utils.terminals import get_terminals
from coevolutionary.manager import CompetitiveManager
from coevolutionary.metrics import Metrics
from coevolutionary.algorithms.gep import GEPAlgorithm
from coevolutionary.algorithms.de import DEAlgorithm
from coevolutionary.utils.tests import check_wilcoxon

# optimization variant '(abcd?|dcba?)[0-9]?'
INPUT_REGEX = '(abcd|abc|dcba|dcb)|(abcd[0-9]|abc[0-9]|dcba[0-9]|dcb[0-9])'

ALGORITHMS = [
    # GEP
    {
        'type': 'gep',
        'population_length': 10,
        'genes_n': 3,
        'head_n': 2,
        'n_elites': 1,
        'metric_type': 1,
    },
    {
        'type': 'gep',
        'population_length': 10,
        'genes_n': 3,
        'head_n': 2,
        'n_elites': 1,
        'metric_type': 2,
    },
    {
        'type': 'gep',
        'population_length': 10,
        'genes_n': 3,
        'head_n': 2,
        'n_elites': 1,
        'metric_type': 3,
    },
    {
        'type': 'gep',
        'population_length': 10,
        'genes_n': 3,
        'head_n': 2,
        'n_elites': 1,
        'metric_type': 4,
    },
    # DE
    {
        'type': 'de',
        'ndim': 10 * 2,
        'bounds': [0, 11],
        'cr': 0.45,
        'f': 1.0,
        'mu': 10,
        'metric_type': 1,
    },
    {
        'type': 'de',
        'ndim': 10 * 2,
        'bounds': [0, 11],
        'cr': 0.45,
        'f': 1.0,
        'mu': 10,
        'metric_type': 2,
    },
    {
        'type': 'de',
        'ndim': 10 * 2,
        'bounds': [0, 11],
        'cr': 0.45,
        'f': 1.0,
        'mu': 10,
        'metric_type': 3,
    },
    {
        'type': 'de',
        'ndim': 10 * 2,
        'bounds': [0, 11],
        'cr': 0.45,
        'f': 1.0,
        'mu': 10,
        'metric_type': 4
    },
]

_excluded_algorithms = ['de']


CM_MANAGER_PARAMETERS = [
    {
        'shared_resource': 500,
        'social_card': 0.3,
        'penalty': 0.1,
        'adaptive_interval': 5
    },
]


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

        # terminals (get by input regex)
        8: 'a',
        9: 'b',
        10: 'c',
        11: 'd',
    }

    test_strings = Utils.get_test_strings(
        input_regex=input_regex,
        n_fuzzy_strings=5,
        terminals=['a', 'b', 'c', 'd'],
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
        custom_symbols=['a', 'b', 'c', 'd', 'any', 'range']
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


def choose_algorithm(
        rows,
        labels,
        _terminals,
        _params,
        _nodes,
        _algorithm_params,
):
    _alg_object = None
    match _algorithm_params.get("type"):
        case 'gep':
            _alg_object = GEPAlgorithm(
                X=rows,
                Y=labels,
                n_iter=100,
                terminals=_terminals,
                params=_params,
                metric_type=_algorithm_params.get('metric_type')
            )
        case 'de':
            _alg_object = DEAlgorithm(
                nodes=_nodes,
                params=_params,
                X=X,
                Y=Y,
                n_iter=100,
                metric_type=_algorithm_params.get('metric_type')
            )
        case _:
            raise NotImplementedError
    return _alg_object


if __name__ == '__main__':
    random.seed(456)

    INIT_METRIC, params, nodes, X, Y, terminals = get_init_data()

    numbers_of_individual_alg = [3, 4, 5, 6]
    exp_counter = 0

    for _ in range(10):
        exp_counter = 0
        for number_of_individual_alg in numbers_of_individual_alg:
            exp_counter += 1
            for m_i, manager_case in enumerate(CM_MANAGER_PARAMETERS):
                print(f'### CM MANAGER PARAMS {m_i}')

                for algorithm in ALGORITHMS:
                    if algorithm.get('type') in _excluded_algorithms:
                        continue
                    print(f'### {algorithm.get("type"): <5} ###')
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
                        alg_object = choose_algorithm(
                            rows=X,
                            labels=Y,
                            _terminals=terminals,
                            _params=params,
                            _nodes=nodes,
                            _algorithm_params=algorithm,
                        )

                        cm = add_alg(
                            manager=cm,
                            name=f'{algorithm.get("type")}_{i}_coev_metric_{algorithm.get("metric_type")}',
                            case=algorithm,
                            alg_object=alg_object
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

                        alg_object = choose_algorithm(
                            rows=X,
                            labels=Y,
                            _terminals=terminals,
                            _params=params,
                            _nodes=nodes,
                            _algorithm_params=algorithm,
                        )

                        cm = add_alg(
                            manager=cm,
                            name=f'{algorithm.get("type")}_{i}_sep_metric_{algorithm.get("metric_type")}',
                            case=algorithm,
                            alg_object=alg_object
                        )

                        # overload run
                        cm.run_coevolution()

                        separately_algorithm_history[i] = cm.algorithm_history[0]
                        sep_names.append(f'{algorithm.get("type")}_{i}')

                        try:
                            check_wilcoxon(
                                history_a=cm.algorithm_history,
                                history_b=best_alg_statistics,
                                a_name=f'{algorithm.get("type")}_{i}_sep',
                                b_name=f'best of coevolutionary {algorithm.get("type")}',
                                a_index=0,
                                b_index=i,
                                metric_number=1,
                                metric_name='minimum'
                            )
                        except ValueError:
                            print('Error! x - y is zero for all elements')
