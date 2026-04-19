import os
import requests
from typing import Optional, Literal, List, Any


Continent = Literal["AMERICAS", "ASIA", "EUROPE"]


RIOT_API_KEY = os.environ.get("RIOT_API_KEY")


def GetAccount(continent: Continent, game_name: str, tag_line: str) -> Optional[Any]:
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()


def GetMatchIds(continent: Continent, account: Any) -> Optional[List[str]]:
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{account["puuid"]}/ids?start=0&count=20&api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()


def GetMatch(continent: Continent, match_id: str) -> Optional[Any]:
    continent = continent.upper()
    response = requests.get(f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}")
    if response.status_code == 200:
        return response.json()


def GetParticipant(match: Any, puuid: str) -> Optional[Any]:
    for participant in match["info"]["participants"]:
        if participant["puuid"] == puuid:
            return participant


def SummarizeMatch(match, puuid: str) -> Any:
    return {
        "champions": {
            participant["puuid"]: {
                "championName": participant["championName"],
                "teamPosition": participant["teamPosition"],
            } for participant in match["info"]["participants"]
        },
        "user": next((participant for participant in match["info"]["participants"] if participant["puuid"] == puuid), None)
    }