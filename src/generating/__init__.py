from enum import Enum


class NodesTypes(Enum):
    seq = 0
    atom = 1
    any = 2
    repeat = 3
    alt = 4
    group = 5
    range = 6
    escape = 7