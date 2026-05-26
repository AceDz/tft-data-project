import logging
from pathlib import Path

import pandas as pd

try:
    from src import transform as transform_module
    from src import validate
    from src.load import load
except ImportError:
    import transform as transform_module
    import validate
    from load import load


RAW_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "tft_matches.json"

def run_pipeline():

    df = pd.read_json(RAW_DATA_PATH)
    
    validate.validate_data(df)
    
    df_fact, fact_traits, fact_units = transform_module.transform(df)

    load(df_fact, fact_traits, fact_units)

    logging.info("Pipeline executed successfully.")