import pandas as pd
import logging
import requests
import src.config as config
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from src import errors
from pyrate_limiter import Duration, Rate, Limiter
import os

def extract_local_data(file_path):

    logging.info(f"Extracting data from {file_path}")
    return pd.read_json(file_path)

def is_rate_limit(exception):
    return isinstance(exception, requests.exceptions.HTTPError) and exception.response.status_code == 429

limiter = Limiter(Rate(80, Duration.MINUTE))
 
class RiotClient:
    
    def __init__(self):
        self.headers = config.HEADERS
        self.region = config.REGION
         
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10), retry = retry_if_exception(is_rate_limit))    
    def _get(self, url: str) -> dict:
        logging.info(f"Calling URL: {url}")
        limiter.try_acquire("riot_api")
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
    