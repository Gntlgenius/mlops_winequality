# load the train and test
# train algo
# save the metrices, params
import os
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from get_data import read_params
import argparse
import joblib
import json


def evaluate_metrics(actual_val, pred_val):
    rmse = np.sqrt(mean_squared_error(actual_val, pred_val))
    mae = mean_absolute_error(actual_val, pred_val)
    r2 = r2_score(actual_val, pred_val)

    return rmse, mae, r2


def training_evaluation(config_path):
    config = read_params(config_path)

    train_path = config["split_data"]["train_path"]
    test_path = config["split_data"]["test_path"]
    random_state = config["base"]["random_state"]
    alpha= config["estimators"]["ElasticNet"]["params"]["alpha"]
    l1_ratio= config["estimators"]["ElasticNet"]["params"]["l1_ratio"]
    model_dir =config["model_dir"]
    target_col = config["base"]["target_col"]

    train_data = pd.read_csv(train_path, sep=",")
    test_data = pd.read_csv(test_path, sep=",")

    X_train = train_data.drop(target_col, axis=1)
    y_train = train_data[target_col]

    X_test = test_data.drop(target_col, axis=1)
    y_test = test_data[target_col]

    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_state)
    lr.fit(X_train, y_train)

    predicted_val = lr.predict(X_test)

    rmse, mae, r2 = evaluate_metrics(y_test, predicted_val)

    print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    scores_file = config["reports"]["scores"]
    params_file = config["reports"]["params"]

    with open(scores_file, "w") as f:
        scores = {
            "rmse": rmse,
            "mae": mae,
            "r2": r2
        }
        json.dump(scores, f, indent=4)

    with open(params_file, "w") as f:
        params = {
            "alpha": alpha,
            "l1_ratio": l1_ratio,
        }
        json.dump(params, f, indent=4)


    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(lr, model_path)

    

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    training_evaluation(config_path=parsed_args.config)