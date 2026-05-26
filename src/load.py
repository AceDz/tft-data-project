from pathlib import Path


PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"


def load(df_fact, fact_traits, fact_units):
    df_fact.to_parquet(PROCESSED_DIR / "fact.parquet", index=False)
    fact_traits.to_parquet(PROCESSED_DIR / "fact_traits.parquet", index=False)
    fact_units.to_parquet(PROCESSED_DIR / "fact_units.parquet", index=False)
    