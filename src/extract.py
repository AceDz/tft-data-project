import pandas as pd
import logging
import requests
import src.config as config

def extract_local_data(file_path):

    logging.info(f"Extracting data from {file_path}")
    return pd.read_json(file_path)
    
def get_puuid(game_name: str, tag_line: str):
    url = f"https://{config.REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    resp = requests.get(url, headers=config.HEADERS)
    resp.raise_for_status()

    data = resp.json()
    return data.get("puuid")

def get_match_ids(puuid: str, count: int = 20):
    url = f"https://{config.REGION}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={count}"
    resp = requests.get(url, headers=config.HEADERS)
    resp.raise_for_status()
    return resp.json()

def get_match_data(match_id: str):
    url = f"https://{config.REGION}.api.riotgames.com/tft/match/v1/matches/{match_id}"
    resp = requests.get(url, headers=config.HEADERS)
    resp.raise_for_status()
    return resp.json()