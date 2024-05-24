# Written by https://github.com/worldbeater

from peco import parse
from parsing import regex
from interpreter import matches


def test():
    state = parse('color: #[0-9A-Fa-f]{6}', regex)
    tree = state.stack[-1]
    assert matches('color: #CEFA70 123 12 3123 123 ', tree) == ' 123 12 3123 123 '
    assert matches('color: #CEFA70', tree) == ''
    assert matches('33333 color: #CEFA70', tree) == '33333 '
    assert matches('color: #F7F590', tree) == ''
    assert matches('color: #CECECEe', tree) == 'e'
    assert matches('color', tree) is None
    assert matches('', tree) is None
    assert matches('color: #QEFA70', tree) is None
