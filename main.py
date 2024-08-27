import pprint
import argparse

from src.translator import Translator
from src.generating.matrix import MatrixGenerator
from src.logger import logger
from src.utils import get_pretty_ast

IS_PPRINT = False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate regular expression')
    parser.add_argument('-r', '--regex', type=str, help='input regex')
    parser.add_argument('-i', '--input', nargs='?', type=str, default='python', help='input syntax of input regex')
    parser.add_argument('-o', '--output', nargs='?', type=str, default='python', help='output syntax')

    args = parser.parse_args()

    translator = Translator()

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
        logger.info(f'--- Get AST:\n{translator.ast}')
        logger.info(f'--- Get AST:\n{get_pretty_ast(translator.ast)}')


