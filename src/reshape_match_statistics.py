import os
import pandas as pd

# Load the CSV
input_path = "data/processed/match_statistics.csv"
df = pd.read_csv(input_path)

# Convert 'value' to numeric (ignore errors like "None", %, etc.)
df["value"] = pd.to_numeric(df["value"], errors="coerce")

# Pivot to get stats per team per match
pivoted = df.pivot_table(index=["fixture_id", "team"],
                         columns="stat_type",
                         values="value",
                         aggfunc="first").reset_index()

# Only keep fixtures with two teams
valid_fixtures = pivoted["fixture_id"].value_counts()[lambda x: x == 2].index
valid_stats = pivoted[pivoted["fixture_id"].isin(valid_fixtures)]

# Sort for consistent pairing
valid_stats = valid_stats.sort_values(["fixture_id", "team"])

# Extract home and away rows
home_stats = valid_stats.groupby("fixture_id").nth(0).reset_index()
away_stats = valid_stats.groupby("fixture_id").nth(1).reset_index()

# Drop unnecessary 'index' columns if present
home_stats = home_stats.loc[:, ~home_stats.columns.str.startswith("index")]
away_stats = away_stats.loc[:, ~away_stats.columns.str.startswith("index")]

# Rename columns
home_stats = home_stats.add_prefix("home_")
away_stats = away_stats.add_prefix("away_")

# Merge into wide format
wide_df = pd.merge(
    home_stats.rename(columns={"home_fixture_id": "fixture_id"}),
    away_stats.rename(columns={"away_fixture_id": "fixture_id"}),
    on="fixture_id"
)

# Save output
output_path = "data/processed/wide_match_statistics.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
wide_df.to_csv(output_path, index=False)
print(f"✅ Saved wide-format stats to: {output_path}")
