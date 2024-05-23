# Written by https://github.com/worldbeater

from peco import parse
from parsing import regex
from interpreter import matches


def test():
    state = parse('color: #[0-9A-Fa-f]{6}', regex)
    tree = state.stack[-1]
    assert matches('color: #CEFA70', tree) == ''
    assert matches('color: #F7F590', tree) == ''
    assert matches('color: #CECECEe', tree) == 'e'
    assert matches('color', tree) is None
    assert matches('', tree) is None
    assert matches('color: #QEFA70', tree) is None
