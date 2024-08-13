import pprint
import argparse

from src.translator import Translator
from src.representation.graph import RepresentationGenerator
from src.logger import logger

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
    logger.info(f'--- Get AST:\n{pprint.pformat(translator.ast)}')

    nodes, edges = RepresentationGenerator.get_nodes_and_edges(
        nodes=[],
        edges=[],
        ast=translator.ast,
    )

    logger.info(f'Representations steps:')
    logger.info(f'--- Nodes: {nodes}')
    logger.info(f'--- Edges: {edges}')
