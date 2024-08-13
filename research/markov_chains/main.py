import ast
from pathlib import Path


class Tree:
    def __init__(self, value, *args):
        self.value = value
        self.children = args

    def __repr__(self, depth=1):
        return_string = [str(self.value)]
        for child in self.children:
            return_string.extend(["\n", "-" * (depth + 1), child.__repr__(depth + 1)])
        return "".join(return_string)


def get_tree(tree):
    def get_child(_tree):
        res = []
        for subtree in _tree:
            if isinstance(subtree, int) or isinstance(subtree, str):
                print(f'####---- {subtree}')
                res.append(Tree(subtree))
            else:
                print(f'#### {subtree}')
                res.append(get_child(subtree))
        return Tree(*res)
    return Tree('seq', *[get_child(x) for x in tree if x != 'seq'])


def get_ast_dataset(path: Path):

    def __normalize_ast(tree):
        return ast.literal_eval(tree)[1:]

    with open(path, 'r') as ast_file:
        __lines = ast_file.readlines()
        data = [get_tree(__normalize_ast(x)) for x in __lines if x[0] != '#' and x != '\n']
        comments = [x.replace('# ', '')[:-1] for x in __lines if x[0] == '#' and x != '\n']
    return comments, data


def print_dataset(_comments, _dataset):
    if len(_comments) != len(_dataset):
        raise AttributeError('Lengths of datasets and comments must be equal')
    print('Dataset of ast:')
    for i, comment in enumerate(_comments):
        print(f'--- get regex <{comment}> and his ast: \n<\n{_dataset[i]}\n>\n')


if __name__ == '__main__':
    regexes, dataset = get_ast_dataset(Path('ast'))
    print_dataset(
        _comments=regexes,
        _dataset=dataset
    )
