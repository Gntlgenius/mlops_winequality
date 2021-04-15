# read data from source
# save data to data/raw

import os
import argparse
from get_data import get_data, read_params


def load_and_save(config_path):
    config = read_params(config_path)
    df = get_data(config_path)
    new_col = [col.replace(" ", "_") for col in df.columns]
    df.columns = new_col
    raw_data_path  = config["load_data"]["raw_dataset_csv"]
    df.to_csv(raw_data_path, sep=",", index=False)

    


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)