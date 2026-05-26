import pandas as pd
import logging

def extract_data(file_path):

    logging.info(f"Extracting data from {file_path}")
    return pd.read_json(file_path)
    