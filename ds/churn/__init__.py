from scipy.io.arff import arffread
import pandas as pd
from sklearn.model_selection import train_test_split

from ds import log
from ds.util import numerify_columns, decision_tree, evaluate_by_rank, evaluate_by_pca, best_ranker_accuracy


def characterize(file_name):
    a = arffread.loadarff(file_name)
    df = pd.DataFrame(a[0])
    df = numerify_columns(df)
    X, y = df.loc[:, df.columns != 'LEAVE'], df['LEAVE']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, train_size=0.5)
    decision_tree(X_train, y_train)

    min_cols, max_cols = 3, len(X_train.columns)
    for evaluator in [evaluate_by_rank, evaluate_by_pca]:
        best_evaluated = best_ranker_accuracy(X_train, y_train, evaluator, min_cols, max_cols)
        log.info(f"Best {evaluator}: {best_evaluated}")

