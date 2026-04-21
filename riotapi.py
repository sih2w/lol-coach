import os
import requests
from typing import Optional, Literal, List, Any


Continent = Literal["AMERICAS", "ASIA", "EUROPE"]


RIOT_API_KEY = os.environ.get("RIOT_API_KEY")


def get_account(continent: Continent, game_name: str, tag_line: str) -> Optional[Any]:
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()


def get_match_ids(continent: Continent, puuid: str) -> Optional[List[str]]:
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()


def get_match(continent: Continent, match_id: str) -> Optional[Any]:
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()
