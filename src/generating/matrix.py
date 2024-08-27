import copy
import re
from ast import literal_eval

from src.generating import NodesTypes


class MatrixGenerator:
    allowed_matrix_types = [
        'adjacency',
        'incidence',
    ]

    # R x R, R = len(node_types)
    _adjacency_base_matrix = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]

    clean_params_reg = re.compile(r'[0-9_]|inf')

    @staticmethod
    def eat(ast):
        output = []
        for subgroup in ast:
            if isinstance(subgroup, tuple):
                output.append(MatrixGenerator.eat(subgroup))
            elif isinstance(subgroup, str):
                output.append(subgroup)
        return output

    @staticmethod
    def get_incidence_lists_by_nodes(nodes, root_node='seq'):
        output_lists = []
        root_node = root_node
        for subgroup in nodes:
            if subgroup == 'seq':
                continue
            if isinstance(subgroup, list):
                output_lists += MatrixGenerator.get_incidence_lists_by_nodes(
                    subgroup, root_node
                )
            elif isinstance(subgroup, str):
                output_lists.append(
                    (
                        MatrixGenerator.get_node_id(root_node),
                        MatrixGenerator.get_node_id(subgroup)
                    )
                )
                root_node = subgroup
        return output_lists

    @staticmethod
    def get_node_id(node_name):
        node_name = MatrixGenerator.clean_params_reg.sub('', node_name)
        try:
            if len(node_name) == 1:
                return NodesTypes.params.value
            if node_name == 'seq':
                return 5
            return NodesTypes.__members__.get(node_name).value
        except:
            raise AttributeError(f'Error with {node_name} node')

    @staticmethod
    def get_incidence_matrix(ast):
        # TODO: add incidence matrix generating
        matrix = []
        return matrix

    @staticmethod
    def get_adjacency_matrix(ast, base_matrix):
        matrix = copy.deepcopy(base_matrix)
        incidence_lists = MatrixGenerator.get_incidence_lists(ast)
        for x, y in incidence_lists:
            if y == -1:
                continue
            matrix[x-1][y-1] = 1
        return matrix

    @staticmethod
    def get_incidence_lists(ast):
        nodes = MatrixGenerator.eat(ast)
        incidence_lists = MatrixGenerator.get_incidence_lists_by_nodes(nodes)
        return incidence_lists

    def __call__(self, ast, matrix_type: str):
        matrix_type = matrix_type.lower()
        matrix_allowed_types = MatrixGenerator.allowed_matrix_types
        if matrix_type not in matrix_allowed_types:
            raise NotImplementedError(f'Matrix type for generating must be in {matrix_allowed_types}')

        ast = literal_eval(ast)

        if matrix_type == 'adjacency':
            return MatrixGenerator.get_adjacency_matrix(ast, self._adjacency_base_matrix)
        elif matrix_type == 'incidence':
            return MatrixGenerator.get_incidence_matrix(ast)
