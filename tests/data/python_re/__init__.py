test_data_v1 = {
    'info': 'A test dataset for relt on python library re. '
            'Structure: [id; input_expression; tokens; optimized_tokens; ast; optimized_ast; output_expression]',
    'data': [
        [
            # id
            1,
            # input
            'abc.',
            # tokens
            '<_ATOM_:a><_ATOM_:b><_ATOM_:c><_ANY_CHARACTER_>',
            # optim_tokens
            '<_ATOM_:a><_ATOM_:b><_ATOM_:c><_ANY_CHARACTER_>',
            # ast
            '',
            # optim_ast
            '',
            # output
            'abc.'],
    ],
}
