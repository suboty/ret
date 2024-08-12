READABILITY_LEVELS = {
    'atom': 1,
    'any': 1,
    'escape': 1,
    'alt': 2,
    'group': 3,
    'range': 3,
    'repeat': 3,
}


def get_readability(ast):
    score = 0
    for subtree in ast:
        if isinstance(subtree, str):
            continue
        score += READABILITY_LEVELS.get(subtree[0])
    return score/len(ast)
