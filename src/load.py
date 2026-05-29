from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging

PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
ERROR_DIR = Path(__file__).resolve().parents[1] / "data" / "errors"


def load(df_fact, fact_traits, fact_units):
    df_fact.to_parquet(PROCESSED_DIR / "fact.parquet", index=False)
    fact_traits.to_parquet(PROCESSED_DIR / "fact_traits.parquet", index=False)
    fact_units.to_parquet(PROCESSED_DIR / "fact_units.parquet", index=False)

def load_to_postgres(fact_matches, fact_traits, fact_units):
    
    load_dotenv()

    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")



    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    fact_matches.to_sql("fact_matches", engine, if_exists="append", index=False)
    fact_traits.to_sql("fact_traits", engine, if_exists="append", index=False) 
    fact_units.to_sql("fact_units", engine, if_exists="append", index=False)
    
    logging.info("Data loaded to PostgreSQL successfully.")
        
        
def load_error(error):
    error.to_json("")
    
    