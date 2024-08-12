from tests.data.python_re import test_data_v1

test_data = []

# TODO: add auto creating test_data object

for ex in test_data_v1['data']:
    test_data.append({
        'id': ex[0],
        'input': ex[1],
        'tokens': ex[2],
        'optim_tokens': ex[3],
        'ast': ex[4],
        'optim_ast': ex[5],
        'output': ex[6]
    })
