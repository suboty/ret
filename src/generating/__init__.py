from enum import Enum


class NodesTypes(Enum):
    params = -1
    seq = 0
    atom = 1
    any = 2
    repeat = 3
    alt = 4
    altgroup = 5
    group = 6
    range = 7
    escape = 8
