from src.utils import *
from src.logger import logger


class PopulationGenerator:
    def __init__(
            self,
            number_of_individual,
            number_of_iterations
    ):
        self.number_of_individual = number_of_individual
        self.number_of_iterations = number_of_iterations

    @staticmethod
    def get_group(group_ast):
        return [x for x in group_ast[1]]

    def __call__(self, regex, *args, **kwargs):
        ast = get_ast(regex)
        logger.info(get_regex(ast))
        root_ast = ast[1]
        subtrees = self.get_group(root_ast)

        logger.info(subtrees)
        logger.info(self.get_group(subtrees[3]))
