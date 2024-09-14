import copy
import pprint
import argparse

import exrex

from src.logger import logger
from src.utils import get_pretty_ast
from src.translator import Translator
from src.translator import GeneratorPython
from src.generating.matrix import MatrixGenerator, GeneratorByIncidence
from src.ast_optimizing.population_algorithms import PopulationAlgorithmsOptimizing
from src.metrics.performance import get_performance_metric

IS_PPRINT = False
IS_EXREX = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate regular expression')
    parser.add_argument('-r', '--regex', type=str, help='input regex')
    parser.add_argument('-i', '--input', nargs='?', type=str, default='python', help='input syntax of input regex')
    parser.add_argument('-o', '--output', nargs='?', type=str, default='python', help='output syntax')
    parser.add_argument('-p', '--phrases', nargs='+', help='Test phrases for optimization')

    args = parser.parse_args()

    translator = Translator()
    python_generator = GeneratorPython()
    matrix_generator = MatrixGenerator()
    regex_generator_by_incidence = GeneratorByIncidence()

    input_regex = args.regex

    input_syntax = args.input
    output_syntax = args.output

    if IS_EXREX:
        test_phrases = list(exrex.generate(input_regex))
    else:
        test_phrases = args.phrases

    output_regex = translator.translate(string=input_regex, input_syntax=input_syntax, output_syntax=output_syntax)

    adjacency_matrix = matrix_generator(
        ast=translator.ast,
        matrix_type='adjacency'
    )

    incidence_list, nodes = matrix_generator(
        ast=translator.ast,
        matrix_type='incidence_list'
    )

    logger.info(f'Translate steps:')
    logger.info(f'--- Get Regex in <{input_syntax}> input syntax: {input_regex}')
    logger.info(f'--- Get Regex in <{output_syntax}> output syntax: {output_regex}')
    if IS_PPRINT:
        logger.info(f'--- Get AST:\n{pprint.pformat(translator.ast)}')
    else:
        logger.info(f'--- Get AST:\n{get_pretty_ast(translator.ast)}')
    logger.info(f'--- Get Incidence List:\n{incidence_list}')

    params_dict = copy.deepcopy(matrix_generator.params_dict)
    optimizer = PopulationAlgorithmsOptimizing()
    de_optimizing_incidence_list = optimizer(
        incidence_list=incidence_list,
        params=params_dict,
        nodes=nodes.nodes_types,
        algorithm='de',
        phrases=test_phrases,
    )
    de_tf_value = optimizer.last_tf_value

    params_dict = copy.deepcopy(matrix_generator.params_dict)
    pso_optimizing_incidence_list = optimizer(
        incidence_list=incidence_list,
        params=params_dict,
        nodes=nodes.nodes_types,
        algorithm='pso',
        phrases=test_phrases,
    )
    pso_tf_value = optimizer.last_tf_value

    # as is
    params_dict = copy.deepcopy(matrix_generator.params_dict)
    as_is_regex = regex_generator_by_incidence(
            incidence_list=incidence_list,
            params=params_dict,
            nodes=nodes.nodes_types,
        )
    as_is_performance_metric = get_performance_metric(
        regex=as_is_regex,
        syntax=1,
        n_iter=500
    )
    logger.info('\nAS IS'
                f'\n--- Performance metric = <{as_is_performance_metric}> sec'
                f'\n--- Target function value = <{optimizer.max_solution_value}>'
                f'\n--- AS IS REGEX:\n{output_regex}')

    # DE
    params_dict = copy.deepcopy(matrix_generator.params_dict)
    de_regex = regex_generator_by_incidence(
            incidence_list=de_optimizing_incidence_list,
            params=params_dict,
            nodes=nodes.nodes_types,
        )
    de_performance_metric = get_performance_metric(
        regex=de_regex,
        syntax=1,
        n_iter=500
    )
    logger.info('\nDE'
                f'\n--- Performance metric = <{de_performance_metric}> sec'
                f'\n--- Target function value = <{de_tf_value}>'
                f'\n--- DE REGEX:\n{de_regex}')

    # PSO
    params_dict = copy.deepcopy(matrix_generator.params_dict)
    pso_regex = regex_generator_by_incidence(
        incidence_list=pso_optimizing_incidence_list,
        params=params_dict,
        nodes=nodes.nodes_types,
    )
    pso_performance_metric = get_performance_metric(
        regex=pso_regex,
        syntax=1,
        n_iter=500
    )
    logger.info('\nPSO'
                f'\n--- Performance metric = <{pso_performance_metric}> sec'
                f'\n--- Target function value = <{pso_tf_value}>'
                f'\n--- PSO REGEX:\n{pso_regex}')
