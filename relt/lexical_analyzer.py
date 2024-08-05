import yaml
from pathlib import Path
from yaml.loader import UnsafeLoader

from relt import logger
from relt.utils import Stack
from relt.configs import tokens_config


class LexicalAnalyzerError(Exception):
    ...


class LoadSyntaxYAML(LexicalAnalyzerError):
    ...


class Syntax:
    def __init__(self, name: str):
        self.syntax = self.__load_yaml(
            syntax_path=Path('relt', 'syntaxes', name+'.yaml')
        )

    @staticmethod
    def __load_yaml(syntax_path):
        try:
            with open(syntax_path) as f:
                return yaml.load(f, Loader=UnsafeLoader)
        except Exception as e:
            logger.error(
                message='Error yaml parsing!',
                exc=e,
                raise_exc=LoadSyntaxYAML,
            )


class LexicalAnalyzer:
    def __init__(self, syntax_name):
        self.syntax = Syntax(name=syntax_name).syntax
        self.tokens_config = tokens_config
        self.stack = []

        # inner variables
        self.__cache = None

        # states
        self.atom_state = None
        self.group_state = None
        self.assertion_state = None
        self.ahead_state = None

    @staticmethod
    def __get_atom(name, value):
        return f'<{name}:{value}>'

    def atom(self, symbol: str):
        if symbol.isalpha() or symbol.isdigit():
            return self.__get_atom(
                name=self.tokens_config.get('Atoms')['atom'],
                value=symbol
            )
        else:
            match symbol:
                case _:
                    ...

    def group(self):
        pass

    def ahead(self):
        pass

    def assertion(self):
        pass

    def __call__(self, *args, **kwargs):
        return args, kwargs
