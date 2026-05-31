import os

HEADERS = {
    "X-Riot-Token": os.getenv("RIOT_API_KEY")
}

REGION = "europe"
COUNT = 100