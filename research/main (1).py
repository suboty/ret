import re
import ast
import random
from collections import Counter
from pathlib import Path


class Tree:
    def __init__(self, value, *args):
        self.value = value
        self.children = args
        self.clean_reg = re.compile(r'\-+')

    def __repr__(self, depth=1):
        return_string = [str(self.value)]
        for child in self.children:
            return_string.extend(["\n", "-" * (depth + 1), child.__repr__(depth + 1)])
        return "".join(return_string)

    def get_ind_words(self):
        string = self.__repr__().replace('\n', '')
        return ast.literal_eval('["' + self.clean_reg.sub('", "', string) + '"]')

    def get_levels(self):
        string = self.__repr__().replace('\n', '')
        results = re.findall('\-+', string)
        return Counter(results).most_common()


def get_tree(tree):
    def get_child(_tree):
        res = []
        for subtree in _tree:
            if isinstance(subtree, int) or isinstance(subtree, str):
                res.append(Tree(subtree))
            else:
                res.append(get_child(subtree))
        return Tree(*res)

    return Tree('seq', *[get_child(x) for x in tree if x != 'seq'])


def get_words(tree):
    res = []

    def get_child(_res, _tree):
        for subtree in _tree.children:
            if len(subtree.children) == 1:
                _res.insert(0, subtree.value)
            else:
                _res += get_child(_res, subtree)
        return _res

    return get_child(res, tree)


def get_petals(tree, is_need_values=False):
    def get_value(_tree):
        if isinstance(_tree.children, tuple) and len(_tree.children) == 1:
            if is_need_values:
                return _tree.children[0]
            else:
                return _tree.value
        else:
            return [get_value(child) for child in _tree.children]

    return get_value(tree)


def get_struct_pairs(tree):
    pairs = []

    def get_level_pairs(_pairs, _tree):
        if _tree.children:
            for subtree in _tree.children:
                _pairs.append((str(_tree.value), str(subtree.value)))
                get_level_pairs(_pairs, subtree)

    get_level_pairs(pairs, tree)
    return pairs


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


def generate_ast_regex(base_regex, length, verbose=False):
    # get pairs of constructions
    pairs = get_struct_pairs(base_regex)
    if verbose:
        print(f'Pairs of constructions: {pairs}')

    # get dictionary with constructions possible paths
    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]
    if verbose:
        print(f'Dictionary of pairs: {word_dict}')
    del_keys = []
    for key in word_dict.keys():
        if len(key) == 1 and word_dict[key] == ['atom']:
            del_keys.append(key)
    for key in del_keys:
        del word_dict[key]
    if verbose:
        print(f'Dictionary of pairs after cleaning: {word_dict}')

    chain = ['seq']

    # generate regex by Markov chain
    n_words = length
    keys = [x for x in word_dict.keys()]
    levels_popularity = base_regex.get_levels()

    while len(chain) != n_words:
        try:
            next_struct = random.choice(word_dict[chain[-1]])
        except KeyError:
            next_struct = random.choice(word_dict[random.choice(keys)])
        chain.append(next_struct)

    return chain


def generate_regex(generating_ast):
    res = ''
    for struct in generating_ast:
        print(struct)


if __name__ == '__main__':
    verbose = False
    names, dataset = get_ast_dataset(Path('ast'))
    if verbose:
        print_dataset(
            _comments=names,
            _dataset=dataset
        )

    g_regex = generate_ast_regex(base_regex=dataset[0], length=50, verbose=False)
    print(g_regex)
    # print(generate_regex(g_regex))
