import pandas as pd
import logging
import requests
import src.config as config
from tenacity import retry, stop_after_attempt, wait_exponential
import errors

def extract_local_data(file_path):

    logging.info(f"Extracting data from {file_path}")
    return pd.read_json(file_path)
 
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))    
def get_puuid(game_name: str, tag_line: str):
    """
    Get puuid of a concrete player
    
    Args:
        game_name: Player game name
        tag_line: Player tag line
        
    Returns: 
        Player's puuid
    """
    
    try:
        url = f"https://{config.REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        resp = requests.get(url, headers=config.HEADERS)
        resp.raise_for_status()
        data = resp.json()
        return data.get("puuid")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error HTTP trying to get puuid for {game_name}#{tag_line}")
        errors.save_error_as_log(f"Game Name: {game_name} | Tag Line: {tag_line}", e.response.status_code, str(e))
        raise
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Error connecting to riot API getting puuid for {game_name}#{tag_line}")
        errors.save_error_as_log(f"Game Name: {game_name} | Tag Line: {tag_line}", 0, str(e))
        raise
    
   

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
def get_match_ids(puuid: str, count: int = 20):
    """
    Get a list of the last matches from a player
    
    Args:
        pouid: Player identifier
        count: Number of matches. Default: 20
        
    Returns: 
        List of match ids
    """
    
    try:
        url = f"https://{config.REGION}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={count}"
        resp = requests.get(url, headers=config.HEADERS)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error HTTP trying to get {count} match_ids for PUUID: {puuid}")
        errors.save_error_as_log(f"PUUID: {puuid} | Count: {count}", e.response.status_code, str(e))
        raise
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Error connecting to riot API getting match_ids for puuid {puuid} with count: {count}")
        errors.save_error_as_log(f"PUUID: {puuid} | Count: {count}", 0, str(e))
        raise
        


@retry(stop = stop_after_attempt(3), wait = wait_exponential(multiplier = 2, min = 4, max = 30))
def get_match_data(match_id: str):
    """
    Get the match data
    
    Args:
        match_id: Match identifier
        
    Returns: 
        Match data in json format
    """
    
    try:
        url = f"https://{config.REGION}.api.riotgames.com/tft/match/v1/matches/{match_id}"
        resp = requests.get(url, headers=config.HEADERS)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error HTTP trying to get match with id: {match_id}")
        errors.save_error_as_log(match_id, e.response.status_code, str(e))
        raise
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Error connecting to riot API for match_data: {match_id}")
        errors.save_error_as_log(match_id, 0, str(e))
        raise
