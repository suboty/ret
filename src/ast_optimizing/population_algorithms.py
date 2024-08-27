class PopulationAlgorithmsOptimizing:
    # TODO: refactor class structure

    allowed_algorithms = [
        'de', 'differential evolution',
        'pso', 'particle swarm optimization',
        'fss', 'fish school search'
    ]

    algorithms_params = {
        'DE': {

        },
        'FSS': {

        },
        'PSO': {

        }
    }

    def get_optimizing_ast_by_de(self, ast):
        return ast

    def get_optimizing_ast_by_fss(self, ast):
        return ast

    def get_optimizing_ast_by_pso(self, ast):
        return ast

    def __call__(self, ast, algorithm):
        if algorithm.lower() not in self.allowed_algorithms:
            raise NotImplementedError(f'Optimizing by algorithm {algorithm} is not implemented')
        match algorithm:
            case 'pso' | 'particle swarm optimization':
                return self.get_optimizing_ast_by_pso(ast)
            case 'de' | 'differential evolution':
                return self.get_optimizing_ast_by_de(ast)
            case 'fss' | 'fish school search':
                return self.get_optimizing_ast_by_fss(ast)
