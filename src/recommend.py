from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def recommend_songs(df, cluster, top_n=5):
    """
    Recommend top similar songs within a cluster using cosine similarity
    """

    # Filter cluster data
    cluster_df = df[df["cluster"] == cluster].copy()

    if cluster_df.empty:
        return pd.DataFrame()

    # Select only numeric features (excluding cluster)
    feature_cols = cluster_df.select_dtypes(include=["number"]).columns.tolist()
    if "cluster" in feature_cols:
        feature_cols.remove("cluster")

    features = cluster_df[feature_cols]

    # Compute centroid
    centroid = features.mean().values.reshape(1, -1)

    # Compute similarity
    similarities = cosine_similarity(features, centroid).flatten()

    # Assign similarity score safely
    cluster_df["similarity"] = similarities

    # Sort by similarity
    cluster_df = cluster_df.sort_values(by="similarity", ascending=False)

    return cluster_df.head(top_n)