from src.ast_optimization.population_generating import PopulationGenerator
from src.translator import Translator
from src.logger import logger

if __name__ == '__main__':
    population_generator = PopulationGenerator(
        number_of_individual=10,
        number_of_iterations=10
    )

    translator = Translator()

    input_regex = 'abc(d|e)'

    logger.info(translator.translate(string=input_regex, input_syntax='python', output_syntax='python'))
    logger.info(translator.ast)
