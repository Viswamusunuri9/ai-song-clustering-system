import joblib
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from src.preprocessing import load_data, preprocess
from src.clustering import train_kmeans, save_model
from sklearn.metrics import silhouette_score
import matplotlib
matplotlib.use('TkAgg')

DATA_PATH = "data/raw/rolling_stones_spotify.csv"

def train():
    print("Loading data...")
    df = load_data(DATA_PATH)

    print("Preprocessing...")
    df, X_scaled, scaler = preprocess(df)

    print("Training KMeans...")
    model = train_kmeans(X_scaled, n_clusters=3)
    
    print("Running PCA visualization...")

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    plt.figure(figsize=(8,6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=model.labels_, cmap='viridis')
    plt.title("Cluster Visualization (PCA)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar(label="Cluster")
    plt.show()

    df["cluster"] = model.predict(X_scaled)
    
    for k in [3, 4, 5, 6]:
        model = KMeans(n_clusters=k, random_state=42)
        labels = model.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        print(f"K={k} → Score={score}")

    # Save processed dataset with clusters
    df.to_csv("data/processed/songs_clustered.csv", index=False)
    score = silhouette_score(X_scaled, model.labels_)
    print(f"Silhouette Score: {score}")
    print("\n Saving model...")
    save_model(model)

    print("Done!")

if __name__ == "__main__":
    train()