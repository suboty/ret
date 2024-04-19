from typing import List, Tuple


class ObjectLength:

    def __init__(self):
        self.length_container = {'__filled': False}


class ObjectString(List):
    def __getitem__(self, *args, **kwargs):
        try:
            return super().__getitem__(*args, **kwargs)
        except IndexError:
            item = self.__len__()
            return super().__getitem__(item - 1)


class ExpressionObject:
    def __init__(
            self,
            symbols: str = '',
            name: str = '',
    ):
        self.symbols = symbols
        self.name = name

        self.length_container = ObjectLength()

    def len(self):
        if self.length_container.length_container['__filled'] is False:
            if isinstance(self.symbols, List):
                self.length_container.length_container['expression'] = len(self.symbols)
            else:
                self.length_container.length_container['expression'] = 1
            return self.length_container.length_container
        elif self.length_container.length_container['__filled'] is True:
            return self.length_container.length_container


class GroupObject:
    def __init__(
            self,
            start_symbols: str = '',
            start_name: str = '',
            end_symbols: str = '',
            end_name: str = '',
            delimiter_symbols: str = '',
            delimiter_name: str = '',
    ):
        self.start_symbols = start_symbols
        self.start_name = start_name
        self.end_symbols = end_symbols
        self.end_name = end_name
        self.delimiter_symbols = delimiter_symbols
        self.delimiter_name = delimiter_name

        self.length_container = ObjectLength()

    def len(self):
        if self.length_container.length_container['__filled'] is False:
            if isinstance(self.start_symbols, List):
                self.length_container.length_container['start'] = len(self.start_symbols)
            else:
                self.length_container.length_container['start'] = 1
            if isinstance(self.end_symbols, List):
                self.length_container.length_container['end'] = len(self.end_symbols)
            else:
                self.length_container.length_container['end'] = 1
            if isinstance(self.delimiter_symbols, List):
                self.length_container.length_container['delimiter'] = len(self.delimiter_symbols)
            else:
                self.length_container.length_container['delimiter'] = 1
            return self.length_container.length_container
        elif self.length_container.length_container['__filled'] is True:
            return self.length_container.length_container


class SpecialObject(ExpressionObject):
    pass


class TokenBase:
    # TODO: add validate for meta
    def __init__(
            self,
            token_group: str,
            tokens: List[Tuple],
            schema: str = 'expression',
    ):
        self.__name__ = token_group
        self.schema = schema

        match schema:
            case 'expression':
                self.tokens = [ExpressionObject(*token) for token in tokens]
            case 'group':
                self.tokens = [GroupObject(*token) for token in tokens]
            case 'special':
                self.tokens = [SpecialObject(*token) for token in tokens]


class ResultTokens:
    tokens: List

    def __init__(self, verbose: bool = False):
        self.tokens = []
        self.verbose = verbose
        self._processing_string = []

    def append(self, token, _elements):
        if self.verbose:
            print(token, [chr(_element) for _element in _elements])
        if token != '':
            self.tokens.append(token)
            self._processing_string += _elements
            return

    def get_result_token(self, _string):
        if TokenMapper.list_comparison(_string[:-1:], self._processing_string):
            return self.tokens
        else:
            result_processing_string = ''.join([chr(x) for x in self._processing_string])
            _string = ''.join([chr(x) for x in _string])
            print('ERROR with lexical analysis')
            print(f'--- Done string:        {_string}')
            print(f'--- Processing string:  {result_processing_string}')
            print(f'--- Result tokens: {self.tokens}')

    def __call__(self, *args, **kwargs):
        return self.tokens


class TokenMapper:
    def __init__(self, ):
        self.mappings = {}
        self.mappings_meta = {}
        self.shield_meta_letters = []

        self.numbers_codes = list(range(48, 58))
        self.upper_letters_codes = list(range(65, 91))
        self.lower_letters_codes = list(range(97, 123))

    @staticmethod
    def __encode_string(string):
        try:
            if len(string) > 1:
                return [ord(x) for x in string]
            else:
                return ord(string)
        except TypeError:
            return None

    @staticmethod
    def list_comparison(list_a, list_b):
        if not isinstance(list_a, List) or not isinstance(list_b, List):
            return False
        if not list_a or not list_b:
            return False
        if len(list_a) != len(list_b):
            return False
        else:
            is_equal = True
            for x, y in zip(list_a, list_b):
                if x != y:
                    is_equal = False
                    break
            return is_equal

    def add_mapping(self,
                    token_base: TokenBase):
        _tokens = []

        match token_base.schema:
            case 'expression':
                for token in token_base.tokens:
                    token: ExpressionObject
                    token.symbols = self.__encode_string(token.symbols)
                    if isinstance(token.symbols, List):
                        if 92 in token.symbols:
                            self.shield_meta_letters.append(token.symbols)
                    else:
                        if 92 == token.symbols:
                            self.shield_meta_letters.append(token.symbols)
                    _tokens.append(token)
            case 'group':
                for token in token_base.tokens:
                    token: GroupObject
                    token.start_symbols = self.__encode_string(token.start_symbols)
                    token.end_symbols = self.__encode_string(token.end_symbols)
                    token.delimiter_symbols = self.__encode_string(token.delimiter_symbols)
                    _tokens.append(token)
            case 'special':
                for token in token_base.tokens:
                    token: SpecialObject
                    token.symbols = self.__encode_string(token.symbols)
                    _tokens.append(token)

        self.mappings[token_base.__name__] = _tokens
        self.mappings_meta[token_base.__name__] = token_base.schema

    def mapper(self, string):
        # TODO: add string representation
        _string = ObjectString(self.__encode_string(string + ' '))
        result_tokens = ResultTokens()

        _skip_element = False
        _done = False

        for i, element in enumerate(_string[:-1:]):

            if _skip_element:
                _skip_element = False
                continue

            for key in self.mappings.keys():

                match self.mappings_meta[key]:
                    case 'group':
                        for group in self.mappings[key]:
                            group: GroupObject
                            if group.start_symbols == element:
                                result_tokens.append(group.start_name, [element])
                                _done = True
                                break
                            elif group.end_symbols == element:
                                result_tokens.append(group.end_name, [element])
                                _done = True
                                break
                            elif group.delimiter_symbols == element:
                                result_tokens.append(group.delimiter_name, [element])
                                _done = True
                                break
                            elif self.list_comparison(group.start_symbols,
                                                      _string[i: i+group.len()['start']]):
                                result_tokens.append(group.start_name,
                                                     _string[i: i+group.len()['start']])
                                _done = True
                                _skip_element = True
                                break
                            elif self.list_comparison(group.end_symbols,
                                                      _string[i: i+group.len()['end']]):
                                result_tokens.append(group.end_name,
                                                     _string[i: i+group.len()['end']])
                                _done = True
                                _skip_element = True
                                break
                            elif self.list_comparison(group.delimiter_symbols,
                                                      _string[i: i+group.len()['delimiter']]):
                                result_tokens.append(group.delimiter_name,
                                                     _string[i: i+group.len()['delimiter']])
                                _done = True
                                _skip_element = True
                                break
                    case 'expression':
                        for expression in self.mappings[key]:
                            expression: ExpressionObject
                            if expression.symbols == element:
                                result_tokens.append(expression.name, [element])
                                _done = True
                                break
                            elif self.list_comparison(expression.symbols,
                                                      _string[i: i+expression.len()['expression']]):
                                result_tokens.append(expression.name,
                                                     _string[i: i+expression.len()['expression']])
                                _done = True
                                _skip_element = True
                                break
                    case 'special':
                        for special_expression in self.mappings[key]:
                            special_expression: SpecialObject

                            match special_expression.name:
                                case '<_ESCAPE_FOLLOWING_CHARACTER_>':
                                    if _string[i:i + 1] not in self.shield_meta_letters and element == 92:
                                        result_tokens.append(special_expression.name, [element])
                                        _done = True
                                        break
                                case '<_PARAMETER_#ELEMENT#_>':
                                    if element in self.numbers_codes or \
                                            element in self.lower_letters_codes or \
                                            element in self.upper_letters_codes:
                                        result_tokens.append(
                                            special_expression.name.replace('ELEMENT',
                                                                            chr(element)), [element])
                                        _done = True
                                        break

                if _done:
                    _done = False
                    break

        result = result_tokens.get_result_token(_string=_string)

        if result:
            return result
        else:
            exit(1)


re3_tokens = TokenMapper()

# TODO: add right and auto order for token groups
# by https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap09.html#tag_09_04_08

re3_tokens.add_mapping(
    TokenBase(
        token_group='Groups and ranges',
        tokens=[
            # move to syntax analyzer
            # ('[^', '<_START_NOT_RANGE_GROUP_>', ']', '<_END_NOT_RANGE_GROUP_>', None, None),
            ('(', '<_START_SIMPLE_GROUP_>', ')', '<_END_SIMPLE_GROUP_>', None, None),
            ('{', '<_START_QUANTIFIER_GROUP_>', '}', '<_END_QUANTIFIER_GROUP_>', ',', '<_DELIMITER_QUANTIFIER_GROUP_>'),
            ('[', '<_START_RANGE_GROUP_>', ']', '<_END_RANGE_GROUP_>', '-', '<_DELIMITER_RANGE_GROUP_>'),
        ],
        schema='group'
    )
)

re3_tokens.add_mapping(
    TokenBase(
        token_group='Anchors',
        tokens=[
            ('^', '<_LINE_START_>'),
            (f'{chr(92)}A', '<_STRING_START_>'),
            ('$', '<_LINE_END_>'),
            (f'{chr(92)}Z', '<_STRING_END_>'),
            (f'{chr(92)}b', '<_WORD_BOUNDARY_>'),
            (f'{chr(92)}<', '<_WORD_START_>'),
            (f'{chr(92)}>', '<_WORD_END_>'),
        ],
    )
)

re3_tokens.add_mapping(
    TokenBase(
        token_group='Character Classes',
        tokens=[
            (f'{chr(92)}c', '<CONTROL_CHARACTER>'),  # re.error: bad escape \c at position 2
            (f'{chr(92)}s', '<_WHITE_SPACE_>'),
            (f'{chr(92)}S', '<_NOT_WHITE_SPACE_>'),
            (f'{chr(92)}d', '<_DIGIT_>'),
            (f'{chr(92)}D', '<_NOT_DIGIT_>'),
            (f'{chr(92)}w', '<_WORD_>'),
            (f'{chr(92)}W', '<_NOT_WORD_>'),
        ]
    )
)

re3_tokens.add_mapping(
    TokenBase(
        token_group='Special Characters',
        tokens=[
            (f'{chr(92)}n', '<_NEW_LINE_>'),
            (f'{chr(92)}r', '<_CARRIAGE_RETURN_>'),
            (f'{chr(92)}t', '<_TAB_>'),
            (f'{chr(92)}v', '<_VERTICAL_TAB_>'),
            (f'{chr(92)}f', '<_FORM_FEED_>'),
            (f'{chr(92)}xxx', '<_OCTAL_CHARACTER_>'),
            (f'{chr(92)}xhh', '<_HEX_CHARACTER_>'),
        ],
    )
)

re3_tokens.add_mapping(
    TokenBase(
        token_group='Assertions',
        tokens=[
            ('?=', '<_LOOKAHEAD_>'),
            ('?!', '<_NEGATIVE_LOOKAHEAD_>'),
            ('?<=', '<_LOOKBEHIND_>'),
            ('?!=', '<_NEGATIVE_LOOKBEHIND_>'),
            ('?<!', '<_NEGATIVE_LOOKBEHIND_>'),
            ('?>', '<_ONLY_ONE_SUBEXPRESSIONS_>'),
            ('?()', '<_CONDITION_IF_THEN_>'),
            ('?()|', '<_CONDITION_IF_THEN_ELSE_>'),
            ('?#', '<_COMMENT_>'),
        ]
    )
)

re3_tokens.add_mapping(
    TokenBase(
        token_group='Expressions quantifiers',
        tokens=[
            ('*', '<_0_OR_MORE_>'),
            ('+', '<_1_OR_MORE_>'),
            ('?', '<_0_OR_1>'),
        ]
    )
)

re3_tokens.add_mapping(
    TokenBase(
        token_group='Escape Sequences',
        tokens=[
            (f'{chr(92)}Q', '<_BEGIN_LITERAL_SEQUENCE_>'),
            (f'{chr(92)}E', '<_END_LITERAL_SEQUENCE_>'),
        ]
    )
)

re3_tokens.add_mapping(
    TokenBase(
        token_group='Special',
        tokens=[
            (None, '<_PARAMETER_#ELEMENT#_>'),
            (f'{chr(92)}', '<_ESCAPE_FOLLOWING_CHARACTER_>'),
        ],
        schema='special'
    )
)
