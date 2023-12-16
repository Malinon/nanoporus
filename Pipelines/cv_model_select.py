import warnings
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from functools import partial

def find_best_model(splited_data, pipe, param, use_yield = True):
    model = GridSearchCV(pipe, param, cv=5)
    label_train, label_test = splited_data.get_labels(use_yield)
    model.fit(splited_data.train_dgms, label_train)
    return model

find_best_model_rf = partial(find_best_model,
                            pipe = Pipeline([("Estimator", RandomForestRegressor(n_estimators=200))])
                            ,param= [{"Estimator__max_features": [0.3, 0.5, 0.8, 0.9, 1.0], "Estimator__max_depth": [3,4,6,8]}])


def find_best_model_lasso(splited_data, use_yield=True):
    warnings.filterwarnings('ignore')
    # Prepare search grid
    pipe = Pipeline([("Estimator", Lasso(max_iter=20000))])
    param = [{"Estimator__alpha": [0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 15.0]}]
    # Find best model
    return find_best_model(splited_data, pipe, param, use_yield)
