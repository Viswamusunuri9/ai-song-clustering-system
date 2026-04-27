from sklearn.metrics.pairwise import cosine_similarity

def recommend_songs(df, cluster, n=5):
    cluster_df = df[df["cluster"] == cluster]

    features = cluster_df.select_dtypes(include=["number"]).drop(columns=["cluster"])

    # Use centroid similarity
    centroid = features.mean().values.reshape(1, -1)
    similarities = cosine_similarity(features, centroid)

    cluster_df["score"] = similarities

    return cluster_df.sort_values(by="score", ascending=False).head(n)