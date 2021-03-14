import pandas as pd
import numpy as np
from scipy.io.arff import arffread
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, cross_val_score
from sklearn.feature_selection import RFE
from sklearn.pipeline import Pipeline

if __name__ == '__main__':
    a = arffread.loadarff('../data/churn.arff')
    churn = pd.DataFrame(a[0])
    type_map = {}
    for c in churn.columns:
        if churn[c].dtype.name == 'object':
            churn[c] = churn[c].apply(lambda x: x.decode('utf8'))
            type_map[c] = ['empty'] + list(churn[c].unique())
            churn.loc[churn[c].isna(), c] = type_map[c][0]
            churn[c] = churn[c].apply(lambda l: type_map[c].index(l))
            churn[c].astype(int)
    X, y = churn.loc[:, churn.columns != 'LEAVE'], churn['LEAVE']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, train_size=0.5)
    classer = DecisionTreeClassifier()
    print(f"churn columns: {churn.columns}")
    result = classer.fit(X_train, y_train)
    print(f"CLASSER RESULT: {result}")
    important_cols = [c for i, c in enumerate(X.columns) if result.feature_importances_[i] > 0.07]
    print(f"CLASSER IMPORTANT COLUMNS: {important_cols}")

    min_cols = 3
    max_cols = len(X_train.columns)
    print(f"Calculating accuracy of {min_cols} to {max_cols} ranked columns")
    for feature_count in range(min_cols, max_cols):
        ranker = RFE(DecisionTreeClassifier(), n_features_to_select=feature_count)
        ranks = ranker.fit(X_train, y_train)
        # print(f"RANKER {ranks.support_}")

        model = DecisionTreeClassifier()
        pipeline = Pipeline(steps=[('s', ranker), ('m', model)])

        # evaluate model
        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=1)
        n_scores = cross_val_score(pipeline, X, y, scoring='accuracy', cv=cv, n_jobs=-1, error_score='raise')
        # report performance
        print(f"RANKER COLS {X_train.columns[ranks.support_]}")
        print(f'{feature_count} Features: Accuracy: {np.mean(n_scores):.3f} ({np.std(n_scores):.3f})')
