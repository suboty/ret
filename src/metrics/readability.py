from src.syntax_analysis.analyzer import SyntaxAnalyzer
from src.lexical_analysis.python import LexicalAnalyzer as LexicalAnalyzerPython


constructions_diff = {
    'atom': 1,
    'any': 1,
    'escape': 1,
    'alt': 2,
    'group': 3,
    'range': 3,
    'repeat': 3
}

sa = SyntaxAnalyzer()

# for Python Dialect
la_python = LexicalAnalyzerPython()


def eat(ast, nodes):
    for subgroup in ast:
        if isinstance(subgroup, str):
            nodes.append(subgroup)
        else:
            eat(subgroup, nodes)

def get_levels(ast, levels):
    for subgroup in ast:
        if isinstance(subgroup, str):
            pass
        else:
            levels += 1
            levels = get_levels(subgroup, levels)
    return levels

def get_nodes_and_levels(ast):
    levels = -1
    nodes = []

    eat(ast, nodes)
    levels = get_levels(ast, levels)
    return nodes, levels

def get_readability(regex, syntax):
    constructions = list(constructions_diff.keys())
    metric = 0
    # TODO: add syntax ids mapping
    if syntax == 1:
        tokens = la_python(regex=regex)
        ast = sa(tokens=tokens)
        print(ast)
        nodes, levels = get_nodes_and_levels(
            ast=ast,
        )
        print(nodes, levels)
        for node in nodes:
            node = node.split('_')[0]
            if node not in constructions:
                continue
            metric += constructions_diff[node]
        return metric * levels
    else:
        raise NotImplementedError(f'Syntax {syntax} is not implemented')