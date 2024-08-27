import pprint
import argparse

from src.logger import logger
from src.utils import get_pretty_ast
from src.translator import Translator
from src.translator import GeneratorPython
from src.ast_optimizing.population_algorithms import PopulationAlgorithmsOptimizing
from src.metrics.performance import get_performance_metric

IS_PPRINT = False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate regular expression')
    parser.add_argument('-r', '--regex', type=str, help='input regex')
    parser.add_argument('-i', '--input', nargs='?', type=str, default='python', help='input syntax of input regex')
    parser.add_argument('-o', '--output', nargs='?', type=str, default='python', help='output syntax')

    args = parser.parse_args()

    translator = Translator()
    optimizer = PopulationAlgorithmsOptimizing()
    python_generator = GeneratorPython()

    input_regex = args.regex

    input_syntax = args.input
    output_syntax = args.output

    output_regex = translator.translate(string=input_regex, input_syntax=input_syntax, output_syntax=output_syntax)

    logger.info(f'Translate steps:')
    logger.info(f'--- Get regex in <{input_syntax}> input syntax: {input_regex}')
    logger.info(f'--- Get Regex in <{output_syntax}> output syntax: {output_regex}')
    if IS_PPRINT:
        logger.info(f'--- Get AST:\n{pprint.pformat(translator.ast)}')
    else:
        logger.info(f'--- Get AST:\n{get_pretty_ast(translator.ast)}')

    de_optimizing_ast = optimizer(
        ast=translator.ast,
        algorithm='de'
    )

    fss_optimizing_ast = optimizer(
        ast=translator.ast,
        algorithm='fss'
    )

    pso_optimizing_ast = optimizer(
        ast=translator.ast,
        algorithm='pso'
    )

    # as is
    as_is_performance_metric = get_performance_metric(
        regex=python_generator(ast=translator.ast),
        syntax=1,
        n_iter=500
    )
    logger.info('\nAS IS'
                f'\n--- Performance metric = <{as_is_performance_metric}> sec'
                f'\n--- AS IS AST:\n{get_pretty_ast(translator.ast)}')

    # DE
    de_performance_metric = get_performance_metric(
        regex=python_generator(ast=de_optimizing_ast),
        syntax=1,
        n_iter=500
    )
    logger.info('\nDE'
                f'\n--- Performance metric = <{de_performance_metric}> sec'
                f'\n--- TO BE DE AST:\n{get_pretty_ast(de_optimizing_ast)}')

    # FSS
    fss_performance_metric = get_performance_metric(
        regex=python_generator(ast=fss_optimizing_ast),
        syntax=1,
        n_iter=500
    )
    logger.info('\nFSS'
                f'\n--- Performance metric = <{fss_performance_metric}> sec'
                f'\n--- TO BE FSS AST:\n{get_pretty_ast(fss_optimizing_ast)}')

    # PSO
    pso_performance_metric = get_performance_metric(
        regex=python_generator(ast=pso_optimizing_ast),
        syntax=1,
        n_iter=500
    )
    logger.info('\nPSO'
                f'\n--- Performance metric = <{pso_performance_metric}> sec'
                f'\n--- TO BE PSO AST:\n{get_pretty_ast(pso_optimizing_ast)}')
