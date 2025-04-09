import requests
import pandas as pd
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv()
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}


# Define the competitions we want
COMPETITIONS = {
    "PL": "Premier League",
    "PD": "La Liga",
    "WC": "World Cup",
    "EC": "Euro",
    "NATIONS": "Nations League"
}

SEASONS = list(range(2024, 2025))  # recent seasons only

def fetch_matches_for_competition(code, year):
    url = f"{BASE_URL}/competitions/{code}/matches?season={year}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed for {code} {year}: {response.status_code}")
        print("Response:", response.text)  # TEMPORARY debug
        return []
    matches = response.json().get("matches", [])
    return matches

def flatten_match_data(match):
    score = match.get("score", {}).get("fullTime", {})
    return {
        "date": match.get("utcDate"),
        "competition": match.get("competition", {}).get("name"),
        "home_team": match.get("homeTeam", {}).get("name"),
        "away_team": match.get("awayTeam", {}).get("name"),
        "home_score": score.get("homeTeam"),
        "away_score": score.get("awayTeam"),
        "status": match.get("status")
    }

def download_all_matches():
    all_matches = []
    for code in COMPETITIONS:
        for year in SEASONS:
            print(f"Fetching {COMPETITIONS[code]} {year}")
            matches = fetch_matches_for_competition(code, year)
            all_matches.extend([flatten_match_data(m) for m in matches])
            sleep(1)  # Respect rate limits
    df = pd.DataFrame(all_matches)
    df.to_csv("data/processed/api_matches.csv", index=False)
    print("Saved to data/processed/api_matches.csv")

if __name__ == "__main__":
    print("API KEY:", API_KEY)  # TEMPORARY
    download_all_matches()
