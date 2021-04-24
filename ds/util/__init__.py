import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from ds import log


def decision_tree(X, y, importance_threshold=0.07):
    classer = DecisionTreeClassifier()
    log.debug(f"churn columns: {X.columns}")
    result = classer.fit(X, y)
    log.debug(f"CLASSER RESULT: {result}")
    important_cols = [c for i, c in enumerate(X.columns) if result.feature_importances_[i] > importance_threshold]
    log.debug(f"CLASSER IMPORTANT COLUMNS: {important_cols}")


def evaluate_by_rank(X, y, n_features):
    ranker = RFE(DecisionTreeClassifier(), n_features_to_select=n_features)
    ranks = ranker.fit(X, y)
    selected_columns = list(X.columns[ranks.support_])

    pipeline = Pipeline(steps=[('s', ranker), ('m', DecisionTreeClassifier())])

    # evaluate model
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=1)
    n_scores = cross_val_score(pipeline, X, y, scoring='accuracy', cv=cv, n_jobs=-1, error_score='raise')
    # report performance
    log.debug(f"Accuracy: {np.mean(n_scores):.3f} ({np.std(n_scores):.3f}): COLS {selected_columns}")
    return n_scores, selected_columns


def evaluate_by_pca(X, y, n_features):
    pca = PCA(n_components=n_features)
    pca.fit(X)
    log.debug(pca.explained_variance_ratio_)
    log.debug(pca.singular_values_)
    return pca.score(X, y), 0


def best_ranker_accuracy(X, y, evaluator, min_features=None, max_features=None):
    max_feat = max_features or len(X.columns)
    min_feat = min_features or 1
    log.debug(f"Calculating accuracy of {min_feat} to {max_feat} ranked columns")
    best = None
    for feature_count in range(min_feat, max_feat):
        n_scores, selected_columns = evaluator(X, y, feature_count)
        mean_score = np.mean(n_scores)
        if not best or mean_score > best[0]:
            best = (np.mean(n_scores), selected_columns)

    return best


def best_pca_accuracy(X, y, min_features=None, max_features=None):
    max_feat = max_features or len(X.columns)
    min_feat = min_features or 1
    pca = PCA(n_components=max(max_feat, min_feat), svd_solver='arpack')
    pca.fit(X, y)
    return pca.score(X)


def numerify_columns(df):
    type_map = {}
    for c in df.columns:
        if df[c].dtype.name == 'object':
            df[c] = df[c].apply(lambda x: x.decode('utf8'))
            type_map[c] = ['empty'] + list(df[c].unique())
            df.loc[df[c].isna(), c] = type_map[c][0]
            df[c] = df[c].apply(lambda l: type_map[c].index(l))
            df[c].astype(int)
    return df