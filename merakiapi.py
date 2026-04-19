import requests
from typing import Any, Union


def GetItemById(item_id: Union[str, int]) -> Any:
    response = requests.get(f"https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/items/{item_id}.json")
    if response.status_code == 200:
        return response.json()


def GetChampionByName(champion_name: str):
    response = requests.get(f"https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions/{champion_name}.json")
    if response.status_code == 200:
        return response.json()


def SummarizeItem(item: Any) -> Any:
    return {
        "name": item["name"],
        "shop": item["shop"],
    }


def SummarizeChampion(champion: Any) -> Any:
    return {
        "title": champion["title"],
        "roles": champion["roles"],
        "attributeRatings": champion["attributeRatings"],
        "abilities": champion["abilities"],
    }