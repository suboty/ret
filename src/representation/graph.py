from src.logger import logger


class RepresentationGenerator:
    @staticmethod
    def get_nodes_and_edges(nodes, edges, ast):
        logger.info('------------')
        _last_node = None
        for i, subtree in enumerate(ast):

            try:
                logger.warning(f'{nodes[-1]} -> {subtree}')
                if isinstance(nodes[-1], str) and isinstance(subtree, str) and len(subtree) != 1:
                    edges.append((nodes[-1], subtree))
            except:
                pass

            if isinstance(subtree, str) and len(subtree) > 1:
                if subtree == 'atom':
                    _last_node = subtree
                else:
                    nodes.append(subtree)
            elif isinstance(subtree, str) and len(subtree) == 1:
                if _last_node:
                    nodes.append((_last_node, subtree))
                    _last_node = None
            elif isinstance(subtree, tuple):
                nodes, edges = RepresentationGenerator.get_nodes_and_edges(nodes, edges, subtree)
        return nodes, edges

    @staticmethod
    def get_adjacency_matrix(ast):
        nodes = []
        edges = []
        output_matrix = [[]]
        for i, subtree in enumerate(ast):
            logger.info(subtree)
            logger.info(f'{type(subtree)}|{len(subtree)}')
            if isinstance(subtree, tuple):
                for j, group in enumerate(subtree):
                    logger.info(f'---{group}')
                    logger.info(f'---{type(group)}|{len(group)}')

                    if isinstance(group, str):
                        nodes.append(group)



