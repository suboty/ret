import random

from tqdm import tqdm

from coevolutionary.utils import Utils
from coevolutionary.utils import regex_process
from coevolutionary.utils.terminals import get_terminals
from coevolutionary.manager import CompetitiveManager
from coevolutionary.algorithms.gep import GEPAlgorithm
from coevolutionary.algorithms.de import DEAlgorithm
from coevolutionary.utils.tests import check_wilcoxon


def get_init_data():
    input_regex = '((a|bb?)|(a|ba?)|([0-9]|.ab))'

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
    }

    test_strings = Utils.get_test_strings(
        input_regex=input_regex,
        n_fuzzy_strings=5
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
        custom_symbols=['a', 'b', 'any', 'range', 'escape']
    )

    return _params, _nodes, _X, _Y, _terminals


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

    params, nodes, X, Y, terminals = get_init_data()

    experiment_only_de = 'only_de'
    experiment_only_gep = 'only_gep'
    experiment_gep_de = 'gep_de'

    de_params_cases = [
        {'ndim': 15 * 2, 'bounds': [0, 10], 'cr': 0.3, 'f': 1.6, 'mu': 100},
        {'ndim': 20 * 2, 'bounds': [0, 10], 'cr': 0.3, 'f': 1.6, 'mu': 100},
        {'ndim': 15 * 2, 'bounds': [0, 10], 'cr': 0.4, 'f': 1.8, 'mu': 100},
        {'ndim': 20 * 2, 'bounds': [0, 10], 'cr': 0.4, 'f': 1.8, 'mu': 100},
    ]

    gep_params_cases = [
        {'population_length': 100, 'genes_n': 2, 'head_n': 2, 'n_elites': 3},
        {'population_length': 100, 'genes_n': 3, 'head_n': 2, 'n_elites': 4},
        {'population_length': 100, 'genes_n': 4, 'head_n': 2, 'n_elites': 5},
        {'population_length': 100, 'genes_n': 5, 'head_n': 2, 'n_elites': 10},
    ]

    cm_manager_params = [
        {'shared_resource': 5_000, 'social_card': 0.3, 'penalty': 0.05, 'adaptive_interval': 3},
        {'shared_resource': 10_000, 'social_card': 0.3, 'penalty': 0.1, 'adaptive_interval': 5},
        {'shared_resource': 20_000, 'social_card': 0.3, 'penalty': 0.15, 'adaptive_interval': 10},
    ]

    for m_i, manager_case in enumerate(cm_manager_params):
        print(f'### CM MANAGER PARAMS {m_i}')
        print('### DE ###\n')
        print('coevolution\n')
        # coevolution
        cm = CompetitiveManager(
            adaptive_interval=manager_case['adaptive_interval'],
            shared_resource=manager_case['shared_resource'],
            verbose=False,
            problem='min',
            survive_schema='best',
            social_card=manager_case['social_card'],
            penalty=manager_case['penalty'],
            experiment_name=experiment_only_de,
        )

        for i, de_case in tqdm(enumerate(de_params_cases)):
            de_object = DEAlgorithm(nodes=nodes, params=params, X=X, Y=Y, n_iter=100)
            cm = add_alg(
                manager=cm,
                name=f'de_{i}_coev',
                case=de_case,
                alg_object=de_object
            )
        cm.run_coevolution()

        coevolution_algorithm_history = cm.algorithm_history
        population_qualities_history = cm.population_qualities_history
        coev_names = cm.get_algorithm_names()
        best_alg_statistics = cm.get_winner_statistics()

        cm.save_algorithms_qualities()

        # separately
        print('separately\n')
        separately_algorithm_history = {}
        sep_names = []

        for i, de_case in tqdm(enumerate(de_params_cases)):
            cm = CompetitiveManager(
                adaptive_interval=manager_case['adaptive_interval'],
                shared_resource=manager_case['shared_resource'],
                verbose=False,
                problem='min',
                survive_schema='best',
                social_card=manager_case['social_card'],
                penalty=manager_case['penalty'],
                experiment_name=experiment_only_de,
            )

            de_object = DEAlgorithm(nodes=nodes, params=params, X=X, Y=Y, n_iter=100)

            cm = add_alg(
                manager=cm,
                name=f'de_{i}_sep',
                case=de_case,
                alg_object=de_object
            )

            # overload run
            cm.run_coevolution()

            separately_algorithm_history[i] = cm.algorithm_history[0]
            sep_names.append(f'de_{i}_sep')

            print('\nBest individual: ', cm.get_best_individual())

            check_wilcoxon(
                history_a=cm.algorithm_history,
                history_b=best_alg_statistics,
                a_name=f'de_{i}_sep',
                b_name=f'best of coevolutionary de',
                a_index=0,
                b_index=i,
                metric_number=1,
                metric_name='minimum'
            )

        print('### GEP ###\n')
        print('coevolution\n')
        # coevolution
        cm = CompetitiveManager(
            adaptive_interval=manager_case['adaptive_interval'],
            shared_resource=manager_case['shared_resource'],
            verbose=False,
            problem='min',
            survive_schema='best',
            social_card=manager_case['social_card'],
            penalty=manager_case['penalty'],
            experiment_name=experiment_only_gep,
        )

        for i, gep_case in tqdm(enumerate(gep_params_cases)):
            gep_object = GEPAlgorithm(X=X, Y=Y, n_iter=100, terminals=terminals, params=params,)
            cm = add_alg(
                manager=cm,
                name=f'gep_{i}_coev',
                case=gep_case,
                alg_object=gep_object
            )
        cm.run_coevolution()

        coevolution_algorithm_history = cm.algorithm_history
        population_qualities_history = cm.population_qualities_history
        coev_names = cm.get_algorithm_names()
        best_alg_statistics = cm.get_winner_statistics()

        cm.save_algorithms_qualities()

        # separately
        print('separately\n')
        separately_algorithm_history = {}
        sep_names = []

        for i, gep_case in tqdm(enumerate(gep_params_cases)):
            cm = CompetitiveManager(
                adaptive_interval=manager_case['adaptive_interval'],
                shared_resource=manager_case['shared_resource'],
                verbose=False,
                problem='min',
                survive_schema='best',
                social_card=manager_case['social_card'],
                penalty=manager_case['penalty'],
                experiment_name=experiment_only_gep,
            )

            gep_object = GEPAlgorithm(X=X, Y=Y, n_iter=100, terminals=terminals, params=params,)

            cm = add_alg(
                manager=cm,
                name=f'gep_{i}_sep',
                case=gep_case,
                alg_object=gep_object
            )

            # overload run
            cm.run_coevolution()

            separately_algorithm_history[i] = cm.algorithm_history[0]
            sep_names.append(f'gep_{i}_sep')

            print('\nBest individual: ', cm.get_best_individual())

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

        print('### GEP + DE ###\n')
        print('coevolution\n')
        # coevolution
        cm = CompetitiveManager(
            adaptive_interval=manager_case['adaptive_interval'],
            shared_resource=manager_case['shared_resource'],
            verbose=False,
            problem='min',
            survive_schema='best',
            social_card=manager_case['social_card'],
            penalty=manager_case['penalty'],
            experiment_name=experiment_gep_de,
        )

        for i, gep_case in tqdm(enumerate(gep_params_cases)):
            gep_object = GEPAlgorithm(X=X, Y=Y, n_iter=100, terminals=terminals, params=params, )
            cm = add_alg(
                manager=cm,
                name=f'gep_{i}_coev',
                case=gep_case,
                alg_object=gep_object
            )
        for i, de_case in tqdm(enumerate(de_params_cases)):
            de_object = DEAlgorithm(nodes=nodes, params=params, X=X, Y=Y, n_iter=100)
            cm = add_alg(
                manager=cm,
                name=f'de_{i}_coev',
                case=de_case,
                alg_object=de_object
            )
        cm.run_coevolution()

        coevolution_algorithm_history = cm.algorithm_history
        population_qualities_history = cm.population_qualities_history
        coev_names = cm.get_algorithm_names()
        best_alg_statistics = cm.get_winner_statistics()

        cm.save_algorithms_qualities()

        # separately
        print('separately\n')
        separately_algorithm_history = {}
        sep_names = []

        for i, gep_case in tqdm(enumerate(gep_params_cases)):
            cm = CompetitiveManager(
                adaptive_interval=manager_case['adaptive_interval'],
                shared_resource=manager_case['shared_resource'],
                verbose=False,
                problem='min',
                survive_schema='best',
                social_card=manager_case['social_card'],
                penalty=manager_case['penalty'],
                experiment_name=experiment_gep_de,
            )

            gep_object = GEPAlgorithm(X=X, Y=Y, n_iter=100, terminals=terminals, params=params, )

            cm = add_alg(
                manager=cm,
                name=f'gep_{i}_sep',
                case=gep_case,
                alg_object=gep_object
            )

            # overload run
            cm.run_coevolution()

            separately_algorithm_history[i] = cm.algorithm_history[0]
            sep_names.append(f'gep_{i}_sep')

            print('\nBest individual: ', cm.get_best_individual())

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

        for i, de_case in tqdm(enumerate(de_params_cases)):
            cm = CompetitiveManager(
                adaptive_interval=manager_case['adaptive_interval'],
                shared_resource=manager_case['shared_resource'],
                verbose=False,
                problem='min',
                survive_schema='best',
                social_card=manager_case['social_card'],
                penalty=manager_case['penalty'],
                experiment_name=experiment_gep_de,
            )

            de_object = DEAlgorithm(nodes=nodes, params=params, X=X, Y=Y, n_iter=100)

            cm = add_alg(
                manager=cm,
                name=f'de_{i}_sep',
                case=de_case,
                alg_object=de_object
            )

            # overload run
            cm.run_coevolution()

            separately_algorithm_history[i] = cm.algorithm_history[0]
            sep_names.append(f'de_{i}_sep')

            print('\nBest individual: ', cm.get_best_individual())

            check_wilcoxon(
                history_a=cm.algorithm_history,
                history_b=best_alg_statistics,
                a_name=f'de_{i}_sep',
                b_name=f'best of coevolutionary de',
                a_index=0,
                b_index=i,
                metric_number=1,
                metric_name='minimum'
            )
