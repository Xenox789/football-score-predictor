import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_data(path="data/raw/results.csv", mapping_path="data/raw/former_names.csv"):
    df = pd.read_csv(path)
    df = standardize_team_names(df, mapping_path)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['neutral'] = df['neutral'].astype(int)
    return df


def standardize_team_names(df, mapping_path="data/raw/former_names.csv"):
    name_map = pd.read_csv(mapping_path)

    # Create mapping dictionary
    replace_dict = dict(zip(name_map['former'], name_map['current']))

    # Apply to both home and away teams
    df['home_team'] = df['home_team'].replace(replace_dict)
    df['away_team'] = df['away_team'].replace(replace_dict)

    return df


def preprocess(df):
    le_team = LabelEncoder()
    le_tour = LabelEncoder()

    # Fit on both home and away to have same label set
    all_teams = pd.concat([df['home_team'], df['away_team']])
    le_team.fit(all_teams)
    le_tour.fit(df['tournament'])

    df['home_team_enc'] = le_team.transform(df['home_team'])
    df['away_team_enc'] = le_team.transform(df['away_team'])
    df['tournament_enc'] = le_tour.transform(df['tournament'])

    features = df[[
        'home_team_enc', 'away_team_enc', 'tournament_enc',
        'year', 'month', 'neutral'
    ]]

    targets = df[['home_score', 'away_score']]

    return features, targets, le_team, le_tour
