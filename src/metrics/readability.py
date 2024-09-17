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


def eat(ast, nodes, levels):
    nodes = nodes
    levels = levels
    for subgroup in ast:
        if isinstance(subgroup, str):
             nodes.append(subgroup)
        else:
            levels += 1
            return eat(subgroup, nodes, levels)
    return nodes, levels

def get_readability(regex, syntax):
    constructions = list(constructions_diff.keys())
    metric = 0
    # TODO: add syntax ids mapping
    if syntax == 1:
        tokens = la_python(regex=regex)
        ast = sa(tokens=tokens)
        nodes, levels = eat(
            ast=ast,
            nodes=[],
            levels=-1
        )
        for node in nodes:
            if node not in constructions:
                continue
            metric += constructions_diff[node]
        return metric * levels
    else:
        raise NotImplementedError(f'Syntax {syntax} is not implemented')