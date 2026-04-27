import streamlit as st
import pandas as pd

from src.profiling import create_profiles
from src.recommend import recommend_songs

# ---------------- CONFIG ---------------- #
DATA_PATH = "data/processed/songs_clustered.csv"

st.set_page_config(
    page_title="🎵 Music Intelligence System",
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
    "🎯 Select Music Segment",
    sorted(df["cluster"].unique())
)

# ---------------- SEGMENT NAME ---------------- #
st.subheader("📌 Segment Name")
st.success(cluster_names.get(cluster, "Unknown Segment"))

# ---------------- SEGMENT CHARACTERISTICS ---------------- #
st.subheader("📊 Segment Characteristics")
st.write(descriptions.get(cluster, "No description available"))

# ---------------- SEGMENT DATA ---------------- #
st.subheader("📈 Feature Summary")
st.dataframe(profiles.loc[[cluster]])

# ---------------- RECOMMENDATIONS ---------------- #
st.subheader("🎧 Recommended Songs")

recommendations = recommend_songs(df, cluster)

if not recommendations.empty:

    display_cols = []

    if "name" in recommendations.columns:
        display_cols.append("name")

    if "similarity" in recommendations.columns:
        recommendations["similarity"] = recommendations["similarity"].round(3)
        display_cols.append("similarity")

    # fallback
    if not display_cols:
        st.dataframe(recommendations.head())
    else:
        st.dataframe(recommendations[display_cols])

else:
    st.warning("No songs found for this segment.")