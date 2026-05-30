import pandas as pd
import logging
import requests
import src.config as config
from tenacity import retry, stop_after_attempt, wait_exponential
from src import errors

def extract_local_data(file_path):

    logging.info(f"Extracting data from {file_path}")
    return pd.read_json(file_path)
 
class RiotClient:
    
    def __init__(self):
        self.headers = config.HEADERS
        self.region = config.REGION
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))    
    def _get(self, url: str) -> dict:
        print(f"Calling URL: {url}")
        try:
            resp = requests.get(url, headers = self.headers)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error: {e.response.status_code} for {url}")
            raise
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection error for {url}")
            raise
    
    def get_puuid(self, game_name: str, tag_line: str) -> str:
        url = f"https://{self.region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        data = self._get(url)
        return data.get("puuid")
    
    def get_match_ids(self, puuid: str, count: int = 20) -> list:
        url = f"https://{self.region}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={count}"
        return self._get(url)
    
    def get_match_data(self, match_id: str) -> dict:
        url = f"https://{self.region}.api.riotgames.com/tft/match/v1/matches/{match_id}"
        return self._get(url)