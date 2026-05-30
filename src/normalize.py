import pandas as pd
from src.errors import save_error_as_csv
import datetime
import logging

def normalize_match(match_data):
    
    participants = match_data["info"]["participants"]
    
    match_id = match_data["metadata"]["match_id"]
    
    data_version = match_data["info"]["game_version"]
    
    fact_matches = pd.DataFrame([
        {
            "match_id": match_id,
            "data_version": data_version,
            "puuid": p["puuid"],
            "placement": p["placement"],
            "level": p["level"],
            "gold_left": p["gold_left"],
            "last_round": p["last_round"],
            "total_damage_to_players": p["total_damage_to_players"],
        }
        for p in participants
    ])
    
    
    
    fact_traits = pd.DataFrame([
        {
            "match_id": match_id,
            "puuid": p["puuid"],
            "trait": t["name"],
            "num_units": t["num_units"],
            "style": t["style"],
            "tier_current": t["tier_current"],
            "tier_total": t["tier_total"],      
        }
        for p in participants
        for t in p["traits"]
    ])
    
    fact_units = pd.DataFrame([
        {
            "match_id": match_id,
            "puuid": p["puuid"],
            "unit": u["character_id"],
            "tier": u["tier"],
            "rarity": u["rarity"],
            "items": u["itemNames"],
        }
        for p in participants
        for u in p["units"]
    ])
    
    return fact_matches, fact_traits, fact_units

def validate_and_filter(df, df_name, critical_fields, business_rules = None, error_type = "validation_error"):
    
    mask_nulls = df[critical_fields].isnull().any(axis = 1)
    
    mask_invalid = business_rules if business_rules is not None else pd.Series(False, index = df.index)
    
    df_errors = df[mask_nulls | mask_invalid]
    df_clean = df[~(mask_nulls | mask_invalid)]

    if not df_errors.empty:
        save_error_as_csv(df_errors, error_type, "transformation")
        
    stats = {
        f"{df_name}": {
            "entry" : len(df),
            "correct": len(df_clean),
            "rejected": len(df_errors)
        }
    }
        
    return df_clean, stats
        
def normalize_fact_matches(participants, match_id, data_version):
    df = pd.DataFrame([
        {
            "match_id" : match_id,
            "data_version" : data_version,
            "puuid" : p["puuid"],
            "placement": p["placement"],
            "level":p["level"],
            "gold_left":p["gold_left"],
            "last_round":p["last_round"],
            "total_damage_to_players":p["total_damage_to_players"]
        }
        for p in participants
        ])
    
    business_rules = ~df["placement"].between(1,8) | ~df["level"].between(1,10)
    
    return validate_and_filter(df, "fact_matches",["match_id", "puuid"], business_rules, "fact_matches_validation_error")

def normalize_fact_traits(participants, match_id):
    df= pd.DataFrame([
        {
            "match_id" : match_id,
            "puuid": p["puuid"],
            "trait": t["name"],
            "num_units": t["num_units"],
            "style": t["style"],
            "tier_current": t["tier_current"],
            "tier_total": t["tier_total"],   
        }
        for p in participants
        for t in p["traits"]
    ])
    
        
    return validate_and_filter(df, "fact_traits",["match_id", "puuid", "trait"], error_type="fact_traits_validation_error")

def normalize_fact_units(participants, match_id):
    df = pd.DataFrame([
        {
            "match_id": match_id,
            "puuid": p["puuid"],
            "unit": u["character_id"],
            "tier": u["tier"],
            "rarity": u["rarity"],
            "items": u["itemNames"],
        }
        for p in participants
        for u in p["units"]
    ])
        
    return validate_and_filter(df, "fact_units", ["match_id", "puuid", "unit"], error_type="fact_units_validation_error")


