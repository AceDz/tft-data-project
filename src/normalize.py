import pandas as pd

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