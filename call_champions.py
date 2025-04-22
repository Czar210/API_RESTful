import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_MAPPINGS = {
    "br": {"region": "br1", "routing": "americas"},
    "na": {"region": "na1", "routing": "americas"},
    "lan": {"region": "la1", "routing": "americas"},
    "las": {"region": "la2", "routing": "americas"},
    "euw": {"region": "euw1", "routing": "europe"},
    "eune": {"region": "eun1", "routing": "europe"},
    "tr": {"region": "tr1", "routing": "europe"},
    "ru": {"region": "ru", "routing": "europe"},
    "jp": {"region": "jp1", "routing": "asia"},
    "kr": {"region": "kr", "routing": "asia"},
    "oce": {"region": "oc1", "routing": "sea"},
    "ph": {"region": "ph2", "routing": "sea"},
    "sg": {"region": "sg2", "routing": "sea"},
    "tw": {"region": "tw2", "routing": "sea"},
    "th": {"region": "th2", "routing": "sea"},
    "vn": {"region": "vn2", "routing": "sea"},
}

API_KEY = os.getenv("RIOT_API_KEY")

def get_puuid_by_riot_id(game_name, tag_line, routing_region):
    url = f"https://{routing_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("puuid")
    return None

def get_match_ids(puuid, region, count=10):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def get_match_details(match_id, region):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_jungle_data(game_name, tag_line, server_code, count=10):
    if server_code not in SERVER_MAPPINGS:
        return []

    server_info = SERVER_MAPPINGS[server_code]
    routing_region = server_info["routing"]

    puuid = get_puuid_by_riot_id(game_name, tag_line, routing_region)
    if not puuid:
        return []

    match_ids = get_match_ids(puuid, routing_region, count=count)
    if not match_ids:
        return []

    data_list = []
    player_name_with_tag = f"{game_name}#{tag_line}"

    for match_id in match_ids:
        match_details = get_match_details(match_id, routing_region)
        if not match_details:
            continue

        for participant in match_details["info"]["participants"]:
            if participant.get("puuid") == puuid:
                match_data = (
                    match_id,
                    player_name_with_tag,
                    participant.get("championName", ""),
                    participant.get("kills", 0),
                    participant.get("deaths", 0),
                    participant.get("assists", 0),
                    participant.get("win", False),
                    match_details["info"].get("gameCreation", 0),
                    match_details["info"].get("gameDuration", 0),
                    participant.get("bountyLevel", 0),
                    participant.get("damageDealtToObjectives", 0),
                    participant.get("doubleKills", 0),
                    participant.get("tripleKills", 0),
                    participant.get("goldEarned", 0)
                )
                data_list.append(match_data)
                break

    return data_list