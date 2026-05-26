import os

API_KEY = os.getenv("RIOT_API_KEY", "RGAPI-bb9fa92d-26aa-4df1-9fa6-b43e986387c8")

HEADERS = {
    "X-Riot-Token": API_KEY
}

REGION = "europe"