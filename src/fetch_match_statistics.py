import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

# API config
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-apisports-key": API_KEY
}

# Leagues to fetch from: Premier League = 39, La Liga = 140
LEAGUES = {
    "Premier League": 39,
    #"La Liga": 140
}
SEASON = 2023  # current season

# Fetch fixture IDs of finished matches
def get_fixture_ids(league_id):
    url = f"{BASE_URL}/fixtures"
    params = {
        "league": league_id,
        "season": SEASON,
        "status": "FT"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch fixtures: {response.status_code}")
        return []
    fixtures = response.json().get("response", [])
    return [f["fixture"]["id"] for f in fixtures]

# Fetch statistics for one fixture
def get_statistics(fixture_id):
    url = f"{BASE_URL}/fixtures/statistics?fixture={fixture_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch stats for fixture {fixture_id}: {response.status_code}")
        return []
    return response.json().get("response", [])

# Flatten statistics to rows
def parse_statistics(stats_response, fixture_id):
    rows = []
    for team_stats in stats_response:
        team_name = team_stats["team"]["name"]
        for stat in team_stats["statistics"]:
            rows.append({
                "fixture_id": fixture_id,
                "team": team_name,
                "stat_type": stat["type"],
                "value": stat["value"]
            })
    return rows

# Main function to fetch and save
def fetch_all_statistics():
    all_stats = []
    for league_name, league_id in LEAGUES.items():
        print(f"Fetching fixture IDs for: {league_name}")
        fixture_ids = get_fixture_ids(league_id)
        print(f"Found {len(fixture_ids)} matches.")

        for idx, fixture_id in enumerate(fixture_ids):
            print(f"[{idx+1}/{len(fixture_ids)}] Fetching stats for fixture {fixture_id}")
            stats = get_statistics(fixture_id)
            all_stats.extend(parse_statistics(stats, fixture_id))
            time.sleep(1.2)  # Respect rate limits

    df = pd.DataFrame(all_stats)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/match_statistics.csv", index=False)
    print("Saved to data/processed/match_statistics.csv")

if __name__ == "__main__":
    fetch_all_statistics()
