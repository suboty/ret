import time
import random
import statistics
from typing import Callable, Dict, List, Tuple

# for nano
STUB_VALUE = 1.0


def _sort_by_fitness_value(ind):
    """Only for MEAN framework"""
    try:
        return ind.fitness.values[0]
    except:
        return STUB_VALUE


class CompetitiveManager:
    population_survive_schemas = {
        'first': lambda population, max_number: [ind for ind in population[:max_number]],
        # only for mean framework
        'best': lambda population, max_number: [ind for ind in sorted(
            population[:max_number], key=lambda x: _sort_by_fitness_value(x)
        )]
    }

    allowed_problems = ['min', 'max']

    def __init__(
            self,
            adaptive_interval: int,
            shared_resource: int,
            verbose: bool = False,
            problem: str = 'min',
            survive_schema: str = 'best',
            n_iter: int = 100,
            social_card: float = 0.3,
            penalty: float = 0.05,
            seed: int = 123,
    ) -> None:
        self.algorithms = []
        self.verbose = verbose
        self.n_iter = n_iter

        # coevolution params
        self.adaptive_interval = adaptive_interval
        self.shared_resource = shared_resource
        if problem not in self.allowed_problems:
            raise NotImplementedError(f'This error <{problem}> is not implemented')
        self.problem = problem
        self.survive_schema = survive_schema
        self.social_card = social_card
        self.penalty = penalty

        # storage for algorithm objects
        self.algorithm_objects = []
        # storage for algorithm population numbers
        self.algorithm_population_numbers = {}
        # storage for algorithm statistics
        self.algorithm_statistics = {}
        # storage for algorithm history
        self.algorithm_history = {}
        # storage for winners history
        self.winners_history = []
        # storage for population qualities
        self.population_qualities_history = []

        random.seed(seed)

    def get_current_winner(self) -> Tuple:
        winner = None
        winner_score = None
        algorithm_names = [x[0] for x in self.algorithms]
        for i, algorithm in enumerate(algorithm_names):
            if self.problem == 'min':
                _min = self.algorithm_statistics[i][1]
                if winner_score:
                    if _min < winner_score:
                        winner_score = _min
                        winner = algorithm
                else:
                    winner_score = _min
                    winner = algorithm
            elif self.problem == 'max':
                _max = self.algorithm_statistics[i][0]
                if winner_score:
                    if _max > winner_score:
                        winner_score = _max
                        winner = algorithm
                else:
                    winner_score = _max
                    winner = algorithm
        if self.verbose:
            print(f'Winner: <{winner}>, score: <{winner_score}>')
        return winner, winner_score

    def add_algorithm(
            self,
            name: str,
            init_params: Dict,
            init_algorithm: Callable,
            init_population: Callable,
            get_fitness_population: Callable,
            select_population: Callable,
            recombine_population: Callable,
            mutate_population: Callable,
    ) -> None:
        self.algorithms.append(
            (
                # 0 name of algorithm
                name,
                # 1 init params for algorithm
                init_params,
                # 2 function for init algorithm params
                init_algorithm,
                # 3 function for getting init (zero) population
                init_population,
                # 4 select population
                select_population,
                # 5 recombine population
                recombine_population,
                # 6 mutate population
                mutate_population,
                # 7 calculate fitness function for all individuals
                get_fitness_population,
            )
        )

    def __termination_criteria(self) -> bool:
        return self.shared_resource > 0

    def __adaptation_criteria(self) -> bool:
        for pop_n in self.algorithm_population_numbers.values():
            if pop_n < self.adaptive_interval:
                return True
        return False

    def __get_looser_length(
            self,
            current_length: int,
            social_length: int,
    ) -> int:
        penalty_length = int(current_length * (1 - self.penalty))
        if penalty_length < social_length:
            return social_length
        return penalty_length

    def get_algorithm_names(self):
        return [x[0] for x in self.algorithms]

    def __get_populations_qualities(self) -> List[float]:
        algorithm_names = [x[0] for x in self.algorithms]
        algorithm_scores = []

        for algorithm in algorithm_names:
            q = 0
            for k in range(self.adaptive_interval - 1):
                q_k = (self.adaptive_interval - k) / (k + 1)
                q_k *= 1 if self.winners_history[-(k + 1)][0] == algorithm else 0
                q += q_k
            algorithm_scores.append(q)
        self.population_qualities_history.append(
            tuple(algorithm_scores)
        )
        return algorithm_scores

    def __get_survivors(
            self,
            algorithm_number: int,
            population: List,
            population_qualities: List,
            social_card: int,
    ) -> List:
        if algorithm_number != population_qualities.index(max(population_qualities)):
            population = self.population_survive_schemas[self.survive_schema](
                population,
                self.__get_looser_length(len(population), social_card)
            )
        return population

    @staticmethod
    def __calculate_statistics(population_fitness: List) -> Tuple:
        population_fitness = [x[0] for x in population_fitness]
        _len = len(population_fitness)
        _min = round(min(population_fitness), 6)
        _max = round(max([x for x in population_fitness if x != STUB_VALUE]), 6)
        _mean = round(statistics.mean(population_fitness), 6)
        _stdev = round(statistics.stdev(population_fitness), 6)
        _median = round(statistics.median(population_fitness), 6)
        _cv = round(_stdev / _mean, 3)
        return _len, _min, _max, _mean, _stdev, _median, _cv

    def print_population_statistic(
            self,
            algorithm_names: List,
            phase: str,
    ):
        max_logger_header_length = 0
        algorithms_strings = []
        for i, algorithm in enumerate(algorithm_names):
            log_header = f'Algorithm <{algorithm}> get statistics: \n'
            if len(log_header) > max_logger_header_length:
                max_logger_header_length = len(log_header)
            log_string = log_header
            log_string += f'\tlen: {self.algorithm_statistics[i][0]}'
            log_string += f'\tmin: {self.algorithm_statistics[i][1]}'
            log_string += f'\tmax: {self.algorithm_statistics[i][2]}'
            log_string += f'\tmean: {self.algorithm_statistics[i][3]}'
            log_string += f'\tstdev: {self.algorithm_statistics[i][4]}'
            log_string += f'\tmedian: {self.algorithm_statistics[i][5]}'
            log_string += f'\tcv: {self.algorithm_statistics[i][6]}'
            algorithms_strings.append(log_string)
        print(
            '#' * (max_logger_header_length - (len(phase) + 1)),
            f'{self.algorithm_population_numbers[0]} - {phase}'
        )
        for algorithm_string in algorithms_strings:
            print(algorithm_string)

    def __run_population(
            self,
            algorithm_number: int,
    ) -> None:

        # STEP X.1: select population
        self.algorithms[algorithm_number][4]()

        # STEP X.2: recombine population
        self.algorithms[algorithm_number][5]()

        # STEP X.3: mutate population
        self.algorithms[algorithm_number][6]()

        # STEP X.4: calculate fitness function for all individuals
        population_fitness = self.algorithms[algorithm_number][7]()
        self.shared_resource -= len(population_fitness)

        self.algorithm_statistics[algorithm_number] = self.__calculate_statistics(
            population_fitness
        )

        self.algorithm_history[algorithm_number].append(
            self.algorithm_statistics[algorithm_number]
        )

    def run_coevolution(self) -> None:
        t0 = time.time()
        algorithm_names = [x[0] for x in self.algorithms]

        for i, algorithm in enumerate(algorithm_names):
            # STEP 1: init algorithms
            self.algorithm_objects.append(
                self.algorithms[i][2](self.algorithms[i][1])
            )

            # STEP 2: init zero population
            self.algorithms[i][3]()

            _population_fitness = self.algorithms[i][7](is_init_population=True)
            self.shared_resource -= len(_population_fitness)

            self.algorithm_population_numbers[i] = 1
            self.algorithm_statistics[i] = self.__calculate_statistics(
                _population_fitness
            )
            self.algorithm_history[i] = [self.algorithm_statistics[i]]

        # first metrics
        if self.verbose:
            self.print_population_statistic(
                algorithm_names=algorithm_names,
                phase='init'
            )

        social_lengths = [
            int(len(x.population) * self.social_card)
            for i, x in enumerate(self.algorithm_objects)
        ]

        # STEP 3: while adaptation criteria
        while self.__adaptation_criteria():
            for i, algorithm in enumerate(algorithm_names):
                self.__run_population(
                    algorithm_number=i,
                )
                self.algorithm_population_numbers[i] += 1

            # adaptation metrics
            if self.verbose:
                self.print_population_statistic(
                    algorithm_names=algorithm_names,
                    phase='adaptation'
                )

            winner, winner_score = self.get_current_winner()

            self.winners_history.append(
                (
                    winner,
                    winner_score
                )
            )

        # STEP 4: while termination criteria
        while self.__termination_criteria():
            for i, algorithm in enumerate(algorithm_names):
                self.__run_population(
                    algorithm_number=i,
                )
                self.algorithm_population_numbers[i] += 1

            # coevolutionary metrics
            if self.verbose:
                self.print_population_statistic(
                    algorithm_names=algorithm_names,
                    phase='coevolution'
                )

            winner, winner_score = self.get_current_winner()

            self.winners_history.append(
                (
                    winner,
                    winner_score
                )
            )

            population_qualities = self.__get_populations_qualities()

            for i, algorithm in enumerate(algorithm_names):
                self.algorithm_objects[i].population = self.__get_survivors(
                    algorithm_number=i,
                    population=self.algorithm_objects[i].population,
                    population_qualities=population_qualities,
                    social_card=social_lengths[i]
                )

        print(f'Done in {round(time.time() - t0, 3)} seconds')

    @staticmethod
    def _get_algorithm() -> str:
        return """
        STEP 1: init algorithms
        STEP 2: init zero population for algorithms
        STEP 3: while not adaptation criteria
            STEP 3.1: select population
            STEP 3.2: recombine population
            STEP 3.3: mutate population
            STEP 3.4: get population fitness
        STEP 4: while not termination criteria
            STEP 4.1: select population
            STEP 4.2: recombine population
            STEP 4.3: mutate population
            STEP 4.4: get population fitness
            STEP 4.5: get survivors
        """

    @staticmethod
    def _get_pseudocode() -> str:
        return """
        FOR each population DO
            initialise population Pop_i with random individuals
        END FOR
        FOR each population DO
            calculate fitness Pop_i individuals against all other populations
        END FOR
        WHILE adaptation criteria not satisfied DO
            FOR each population DO
                select individual from Pop_i
                recombine individual
                mutate individual
            END FOR
            FOR each population DO
                calculate fitness Pop_i individuals against all other populations
            END FOR
        END WHILE
        WHILE termination criteria not satisfied DO
            FOR each population DO
                select individual from Pop_i
                recombine individual
                mutate individual
            END FOR
            FOR each population DO
                calculate fitness Pop_i individuals against all other populations
            END FOR
            FOR each population DO
                survivor selection
            END FOR
        END WHILE
        """


class CooperativeManager:
    ...