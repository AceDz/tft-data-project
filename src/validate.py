import logging

def validate_columns(df):
    required_columns = [
        "match_id",
        "player",
        "placement",
        "level",
        "traits",
        "units"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
def validate_nulls(df):
    if df["player"].isnull().any():
        raise ValueError("Null values found in 'player' column")
    if df["match_id"].isnull().any():
        raise ValueError("Null values found in 'match_id' column")
    if df["placement"].isnull().any():
        raise ValueError("Null values found in 'placement' column")
    
def validate_placement(df):
    if not df["placement"].between(1, 8).all():
        raise ValueError("Invalid values found in 'placement' column")
    
def validate_duplicates(df):
    duplicates = df.duplicated(subset=["match_id", "player"])
    if duplicates.any():
        raise ValueError("Duplicate rows found based on 'match_id' and 'player'")
    
def validate_data(df):
    validate_columns(df)
    validate_nulls(df)
    validate_placement(df)
    validate_duplicates(df)

    logging.info("Data validation passed successfully.")