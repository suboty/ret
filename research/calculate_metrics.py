import re

from run import get_init_data
from coevolutionary.metrics import Metrics

if __name__ == '__main__':

    INIT_METRIC, params, nodes, X, Y, terminals = get_init_data()
    new_Y = []
    for target in Y:
        if target:
            new_Y.append(1)
        else:
            new_Y.append(0)
    Y = new_Y

    while True:
        print('--------')
        input_regex = input('Enter regex: ')
        preds = []
        for x in X:
            try:
                _ = re.match(input_regex, x).group(0)
                preds.append(1)
            except:
                preds.append(0)
        tp, fp, fn, tn = Metrics.get_errors_matrix(y_true=Y, y_pred=preds)

        print(Metrics.get_accuracy(tp=tp, fp=fp, fn=fn, tn=tn))
        print(Metrics.get_precision(tp=tp, fp=fp, fn=fn, tn=tn))
        print(Metrics.get_recall(tp=tp, fp=fp, fn=fn, tn=tn))
        print(Metrics.get_f1_score(tp=tp, fp=fp, fn=fn, tn=tn))

