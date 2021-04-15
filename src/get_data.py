## read params
##process
##return dataframe

import os
import yaml
import pandas as pd
import argparse


def get_data(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    print(config)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    get_data(config_path=parsed_args.config)