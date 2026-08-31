import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


scripts_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(scripts_folder)
data_folder = os.path.join(root_folder, "data")
src_folder = os.path.join(root_folder, "src")

if src_folder not in sys.path:
    sys.path.append(src_folder)

from vectors_helper import normalize_vectors

VECTORS_FILE = os.path.join(data_folder, "game_vectors.npz")
PLOT_FILE = os.path.join(data_folder, "silhouette_plot.png")

K_VALUES = [2, 3, 4, 5, 6, 11, 16, 21, 26, 31]
SAMPLE_SIZE = 5000


def build_silhouette_plot():

    data = np.load(VECTORS_FILE)
    matrix = data['vectors']

    vector_norms = np.linalg.norm(matrix, axis=1)
    has_signal = vector_norms > 0
    tagged_matrix = normalize_vectors(matrix[has_signal]).astype('float32')

    scores = []

    for k in K_VALUES:
        print(f"Fitting k-means with k={k}...")
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(tagged_matrix)
        score = silhouette_score(tagged_matrix, labels, sample_size=SAMPLE_SIZE, random_state=42)
        scores.append(score)
        print(f"k={k}: silhouette score = {score:.4f}")

    
    print(f"Saving plot to '{PLOT_FILE}'...")
    plt.figure(figsize=(10,6))
    plt.plot(K_VALUES, scores, marker='o')
    plt.title("Silhouette Score vs. k")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Silhouette score")
    plt.grid(True, alpha=0.3)
    plt.savefig(PLOT_FILE, dpi=150)
    print("Done!")


if __name__ == "__main__":
    build_silhouette_plot()