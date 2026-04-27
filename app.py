import streamlit as st
import pandas as pd

from src.profiling import create_profiles
from src.recommend import recommend_songs

# ---------------- CONFIG ---------------- #
DATA_PATH = "data/processed/songs_clustered.csv"

st.set_page_config(
    page_title="🎵 Song Clustering System",
    layout="centered"
)

# ---------------- TITLE ---------------- #
st.title("🎵 Music Intelligence & Segmentation System")

# ---------------- LOAD DATA ---------------- #
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# ---------------- CREATE PROFILES ---------------- #
profiles, descriptions, cluster_names = create_profiles(df)

# ---------------- CLUSTER SELECTION ---------------- #
cluster = st.selectbox(
    "Select Music Segment",
    sorted(df["cluster"].unique())
)

# ---------------- SEGMENT OVERVIEW ---------------- #
st.subheader("🎯 Segment Overview")
st.write(cluster_names.get(cluster, "Unknown Segment"))

# ---------------- SEGMENT CHARACTERISTICS ---------------- #
st.subheader("📊 Segment Characteristics")
st.write(descriptions.get(cluster, "No description available"))

st.dataframe(profiles.loc[[cluster]])

# ---------------- RECOMMENDATIONS ---------------- #
st.subheader("🎧 Recommended Songs")

songs = recommend_songs(df, cluster)

if songs is not None and not songs.empty:
    if "name" in songs.columns:
        st.dataframe(songs[["name", "cluster"]])
    else:
        st.dataframe(songs.head())
else:
    st.warning("No songs found for this segment.")