"""Set the configs for relt as a python dict."""

import logging
import sys

logging_config = {
    'level': logging.INFO,
    'stream_handler': sys.stdout,
    'format': "%(asctime)s | %(levelname)s]: %(message)s"
}

tokens_config = {
    'Groups': {
        'simple': {
            'start': '_START_SIMPLE_GROUP_',
            'end': '_END_SIMPLE_GROUP_',
        },
        'quantifier': {
            'start': '_START_QUANTIFIER_GROUP_',
            'end': '_END_QUANTIFIER_GROUP_',
            'delimiter': '_DELIMITER_RANGE_GROUP_',
        },
        'range': {
            'start': '_START_RANGE_GROUP_',
            'end': '_END_RANGE_GROUP_',
            'delimiter': '_DELIMITER_RANGE_GROUP_',
            'not': '_NOT_RANGE_GROUP_',
        }
    },

    'Atoms': {
        'atom': '_ATOM_',
        'line_start': '_LINE_START_',
        'string_start': '_STRING_START_',
        'line_end': '_LINE_END_',
        'string_end': '_STRING_END_',
        'word_boundary': '_WORD_BOUNDARY_',
        'word_start': '_WORD_START_',
        'word_end': '_WORD_END_',
        'control_character': '_CONTROL_CHARACTER_',
        'white_space': '_WHITE_SPACE_',
        'not_white_space': '_NOT_WHITE_SPACE_',
        'digit': '_DIGIT_',
        'not_digit': '_NOT_DIGIT_',
        'word': '_WORD_',
        'not_word': '_NOT_WORD_',
        'new_line': '_NEW_LINE_',
        'carriage_return': '_CARRIAGE_RETURN_',
        'tab': '_TAB_',
        'vertical_tab': '_VERTICAL_TAB_',
        'form_feed': '_FORM_FEED_',
        'octal_character': '_OCTAL_CHARACTER_',
        'hex_character': '_HEX_CHARACTER_',
        'begin_literal_sequence': '_BEGIN_LITERAL_SEQUENCE_',
        'end_literal_sequence': '_END_LITERAL_SEQUENCE_',
        'escape_character': '_ESCAPE_FOLLOWING_CHARACTER_',
        'any_character': '_ANY_CHARACTER_',
    },

    'Ahead': {
        '0_or_more': '_0_OR_MORE_',
        '1_or_more': '_1_OR_MORE_',
        '0_or_1': '_0_OR_1'
    },

    'Assertions': {
        'lookahead': '_LOOKAHEAD_',
        'negative_lookahead': '_NEGATIVE_LOOKAHEAD_',
        'lookbehind': '_LOOKBEHIND_',
        'negative_lookbehind': '_NEGATIVE_LOOKBEHIND_',
        'once_only_subexpression': '_ONCE_ONLY_EXPRESSION_',
        'condition_if_then': '_CONDITION_IF_THEN_',
        'condition_if_then_else': '_CONDITION_IF_THEN_ELSE_',
        'comment': '_COMMENT_'
    },
}
