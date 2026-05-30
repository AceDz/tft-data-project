import logging

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

from src.extract import RiotClient
from src.load import load_to_postgres, get_engine
from src.normalize import normalize_fact_matches, normalize_fact_traits, normalize_fact_units
import sys

def run_pipeline(game_name: str, tag_line: str):
    
    client = RiotClient()
    engine = get_engine()
    all_stats = {}
    
    puuid = client.get_puuid(game_name, tag_line)
    match_ids = client.get_match_ids(puuid)
    
    for match_id in match_ids:
        data = client.get_match_data(match_id)
        participants = data["info"]["participants"]
        data_version = data["info"]["game_version"]
        
        fm,stats_fm = normalize_fact_matches(participants, match_id, data_version)
        ft,stats_ft = normalize_fact_traits(participants, match_id)
        fu, stats_fu = normalize_fact_units(participants, match_id)
        
        all_stats.update(stats_fm)
        all_stats.update(stats_ft)
        all_stats.update(stats_fu)
        
        load_to_postgres(fm,ft,fu, engine)
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Use: python pipeline.py <game_name> <tag_line>")
        sys.exit(1)
    
    game_name = sys.argv[1]
    tag_line = sys.argv[2]
    
    run_pipeline(game_name, tag_line)
    
    
