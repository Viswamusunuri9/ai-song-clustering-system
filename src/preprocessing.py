import pandas as pd
from sklearn.preprocessing import StandardScaler

FEATURES = [
    "danceability",
    "energy",
    "loudness",
    "tempo",
    "valence"
]

def load_data(path):
    df = pd.read_csv(path)
    return df

def preprocess(df):
    df = df.dropna(subset=FEATURES)
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")
    
    X = df[FEATURES]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return df, X_scaled, scaler