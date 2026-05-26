import logging

def transform(df):

    df_fact = df[["match_id","player","placement","level"]].copy()

    df_traits = df[["player","traits"]].explode("traits")
    df_traits = df_traits.rename(columns={"traits": "trait"})

    df_units = df[["player","units"]].explode("units")
    df_units = df_units.rename(columns={"units": "unit"})

    fact_traits = df_fact.merge(df_traits, on="player", how="left")
    fact_units = df_fact.merge(df_units, on="player", how="left")

    logging.info("Data transformation completed successfully.")

    return df_fact, fact_traits, fact_units