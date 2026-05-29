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
    
    
def validate_fact_matches(df):
    assert df["match_id"].notnull().all(), "Null values found in 'match_id' column"
    assert df["puuid"].notnull().all(), "Null values found in 'puuid' column"
    assert df["placement"].between(1, 8).all(), "Invalid values found in 'placement' column"
    assert df["level"].between(1, 10).all(), "Invalid values found in 'level' column"
    
    return True
def validate_fact_traits(df):
    assert df["trait"].notnull().all(), "Null values found in 'trait' column"
    assert df["num_units"].between(0, 10).all(), "Invalid values found in 'num_units' column"
    
    return True

def validate_fact_units(df):
    assert df["unit"].notnull().all(), "Null values found in 'unit' column"
    assert df["tier"].between(1, 3).all(), "Invalid values found in 'tier' column"
    
    return True

def validate_consistency(fm, ft, fu):
    
    assert set(fm["puuid"]) == set(ft["puuid"]) == set(fu["puuid"]), "Inconsistent 'puuid' values across dataframes"
    
    return True

def validate_no_duplicates(df, keys):
    assert not df.duplicated(subset=keys).any(), f"Duplicate rows found based on keys: {keys}"
    return True

def validate_all(fm, ft, fu):
    validate_fact_matches(fm)
    validate_fact_traits(ft)
    validate_fact_units(fu)
    validate_consistency(fm, ft, fu)
    validate_no_duplicates(fm, ["match_id","puuid"])
    validate_no_duplicates(ft, ["match_id", "puuid", "trait"])
    validate_no_duplicates(fu, ["match_id", "puuid","unit"])
    
    logging.info("All validations passed successfully.")