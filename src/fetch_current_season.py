import os
import requests
import pandas as pd
from dotenv import load_dotenv
from time import sleep

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

# Define headers and base URL
headers = {
    "x-apisports-key": API_KEY
}
BASE_URL = "https://v3.football.api-sports.io"

# Define leagues and season
LEAGUES = {
    "Premier League": 39,
    "La Liga": 140
}
SEASON = 2023  # Update to the current season

def fetch_matches(league_id):
    url = f"{BASE_URL}/fixtures?league={league_id}&season={SEASON}&status=FT"
    response = requests.get(url, headers=headers)
    print(f"Response Status: {response.status_code}")
    print(f"Response Data: {response.json()}")
    if response.status_code == 200:
        return response.json().get("response", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []


def parse_match(match):
    return {
        "date": match["fixture"]["date"],
        "home_team": match["teams"]["home"]["name"],
        "away_team": match["teams"]["away"]["name"],
        "home_score": match["goals"]["home"],
        "away_score": match["goals"]["away"]
    }

def fetch_all():
    all_matches = []
    for league_name, league_id in LEAGUES.items():
        print(f"Fetching matches for: {league_name}")
        matches = fetch_matches(league_id)
        if not matches:
            print(f"No data found for {league_name} in season {SEASON}.")
            continue
        parsed_matches = [parse_match(m) for m in matches]
        all_matches.extend(parsed_matches)
        sleep(6)  # To respect API rate limits
    if all_matches:
        df = pd.DataFrame(all_matches)
        os.makedirs("data/processed", exist_ok=True)
        df.to_csv("data/processed/current_season_matches.csv", index=False)
        print("Data saved to data/processed/current_season_matches.csv")
    else:
        print("No match data was retrieved.")


if __name__ == "__main__":
    fetch_all()
