from typing import List

from src.logger import logger


class MatrixGenerator:

    allowed_matrix_types = [
        'adjacency',
        'incidence',
    ]

    @staticmethod
    def get_incidence_matrix(ast):
        # TODO: add incidence matrix generating
        matrix = []
        return matrix

    @staticmethod
    def get_adjacency_matrix(ast):
        matrix = []
        return matrix

    def __call__(self, ast, matrix_type: str):
        matrix_type = matrix_type.lower()
        matrix_allowed_types = MatrixGenerator.allowed_matrix_types
        if matrix_type not in matrix_allowed_types:
            raise NotImplementedError(f'Matrix type for generating must be in {matrix_allowed_types}')

        if matrix_type == 'adjacency':
            return MatrixGenerator.get_adjacency_matrix(ast)
        elif matrix_type == 'incidence':
            return MatrixGenerator.get_incidence_matrix(ast)
