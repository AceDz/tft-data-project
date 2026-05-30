from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import os
import logging
from src.errors import save_error_as_log
import pandas as pd

PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
ERROR_DIR = Path(__file__).resolve().parents[1] / "data" / "errors"


def load(df_fact, fact_traits, fact_units):
    df_fact.to_parquet(PROCESSED_DIR / "fact.parquet", index=False)
    fact_traits.to_parquet(PROCESSED_DIR / "fact_traits.parquet", index=False)
    fact_units.to_parquet(PROCESSED_DIR / "fact_units.parquet", index=False)


def get_engine():
    
    try:
        load_dotenv()

        DB_HOST = os.getenv("POSTGRES_HOST")
        DB_PORT = os.getenv("POSTGRES_PORT")
        DB_NAME = os.getenv("POSTGRES_DB")
        DB_USER = os.getenv("POSTGRES_USER")
        DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

        engine = create_engine( f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        logging.info("PostgreSQL connection established successfully.")
        return engine
    except ProgrammingError:
        logging.error(f"Error connecting to PostgreSQL: {e}")
        save_error_as_log("PostgreSQL load", 0, str(e))
        raise
       
def load_to_postgres(fact_matches, fact_traits, fact_units, engine):
    try:
        try:
            existing = pd.read_sql("SELECT DISTINCT match_id FROM fact_matches", engine)
            fact_matches = fact_matches[~fact_matches["match_id"].isin(existing["match_id"])]
            fact_traits = fact_traits[~fact_traits["match_id"].isin(existing["match_id"])]
            fact_units = fact_units[~fact_units["match_id"].isin(existing["match_id"])]
        except Exception:
            logging.info("Tables don't exist yet, loading all data.")
    
        
        if fact_matches.empty:
            logging.info("No new matches to load.")
            return
        
        
        fact_matches.to_sql("fact_matches", engine, if_exists="append", index=False)
        logging.info(f"Loaded {len(fact_matches)} rows to fact_matches")
        fact_traits.to_sql("fact_traits", engine, if_exists="append", index=False) 
        logging.info(f"Loaded {len(fact_traits)} rows to fact_traits")
        fact_units.to_sql("fact_units", engine, if_exists="append", index=False)
        logging.info(f"Loaded {len(fact_units)} rows to fact_units")

        logging.info("Data loaded to PostgreSQL successfully.")
    except Exception as e:
        logging.error(f"Error loading data to PostgreSQL: {e}")
        save_error_as_log("PostgreSQL load", 0, str(e))
        raise
    
    
    
    
        
        
    
    