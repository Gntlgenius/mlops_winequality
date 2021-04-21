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
from urllib.parse import urlparse
import joblib
import json
import mlflow


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

    ##################### #ML FLOW #######################################################
    mlflow_config = config["mlflow_config"]
    remote_server_uri = mlflow_config["remote_server_uri"]
    experiment_name = mlflow_config["experiment_name"]
    run_name = mlflow_config["run_name"]
    registered_model_name = mlflow_config["registered_model_name"]
    remote_server_uri = mlflow_config["remote_server_uri"]

    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=run_name) as mlops_run:

        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_state)
        lr.fit(X_train, y_train)

        predicted_val = lr.predict(X_test)

        rmse, mae, r2 = evaluate_metrics(y_test, predicted_val)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme
        if tracking_url_type_store !="file":
            mlflow.sklearn.log_model(lr, "model", registered_model_name=registered_model_name)
        else:
            mlflow.sklearn.load_model(lr, "model")

    
    

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    training_evaluation(config_path=parsed_args.config)