import numpy


def get_levenshtein_distance(regex_a, regex_b):
    distances = numpy.zeros((len(regex_a) + 1, len(regex_b) + 1))
    for t1 in range(len(regex_a) + 1):
        distances[t1][0] = t1
    for t2 in range(len(regex_b) + 1):
        distances[0][t2] = t2
    for t1 in range(1, len(regex_a) + 1):
        for t2 in range(1, len(regex_b) + 1):
            if regex_a[t1 - 1] == regex_b[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                if a <= b and a <= c:
                    distances[t1][t2] = a + 1
                elif b <= a and b <= c:
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1
    return distances[len(regex_a)][len(regex_b)]
