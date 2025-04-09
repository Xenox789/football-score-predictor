import pandas as pd

# Load the dataset
df = pd.read_csv("data/raw/results.csv")

# Show the first few rows
print(df.head())

# Dataset shape
print("Rows:", len(df))
print("Columns:", df.columns.tolist())

# Check data types and missing values
print(df.info())

# Summary statistics for numerical columns
print(df.describe())

# Unique values in categorical columns
print("Tournaments:", df['tournament'].unique())
print("Countries:", df['country'].nunique())
print("Teams:", df['home_team'].nunique(), "home teams")
print("Teams:", df['away_team'].nunique(), "away teams")
