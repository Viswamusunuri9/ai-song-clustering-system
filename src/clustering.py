from sklearn.cluster import KMeans
import joblib

def train_kmeans(X_scaled, n_clusters=3):
    model = KMeans(n_clusters=n_clusters, random_state=42)
    model.fit(X_scaled)
    return model

def save_model(model, path="models/kmeans.pkl"):
    joblib.dump(model, path)

def load_model(path="models/kmeans.pkl"):
    return joblib.load(path)