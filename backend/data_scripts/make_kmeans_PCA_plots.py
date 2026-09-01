"""
Satisfies:
    - data visualization functionalities for data exploration and inspection
    - functionalities to evaluate the accuracy of the data product
    - a user-friendly, functional dashboard that includes three visualization types (1 of 3)

This script takes creates multiple scatter plots that show the distribution of points in
each closter. PCA flattening is used to turn the 300 dimension vector space into a 2d
space of points, these are plotted by color for each cluster. The difference in cluster
shapes and position shows the accuracy of the k means method applied to data.
"""
import sqlite3
import numpy as np
import os
import sys
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


scripts_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(scripts_folder)
data_folder = os.path.join(root_folder, "data")
src_folder = os.path.join(root_folder, "src")

if src_folder not in sys.path:
    sys.path.append(src_folder)

from vectors_helper import normalize_vectors

VECTORS_FILE = os.path.join(data_folder, "game_vectors.npz")
DB_PATH = os.path.join(data_folder, "steam_games.db")
PLOT_FILE = os.path.join(data_folder, "cluster_plot.png")

K = 6
SAMPLES_PER_CLUSTER = 10

def get_titles(appids):
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    placeholders = ",".join("?" for _ in appids)

    rows = cursor.execute(
        f"SELECT appid, title FROM games WHERE appid IN ({placeholders})", appids).fetchall()

    conn.close()

    return dict(rows)


def inspect_clusters():

    data = np.load(VECTORS_FILE)

    ids = data['ids']
    matrix = data['vectors']

    vector_norms = np.linalg.norm(matrix, axis=1)
    has_signal = vector_norms > 0

    tagged_ids = ids[has_signal]
    tagged_matrix = normalize_vectors(matrix[has_signal]).astype('float32')

    print(f"Fitting k-means with k={K}...")
    kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
    labels = kmeans.fit_predict(tagged_matrix)

    print("\n=== Sample games per cluster ===")
    for cluster_id in range(K):
        cluster_mask = labels == cluster_id
        cluster_ids = tagged_ids[cluster_mask]
        cluster_size = len(cluster_ids)

        sample_ids = cluster_ids[:SAMPLES_PER_CLUSTER].tolist()
        titles = get_titles(sample_ids)

        print(f"\nCluster {cluster_id} ({cluster_size} games):")
        for appid in sample_ids:
            print(f"  - {titles.get(appid, f'[appid {appid} not found]')}")
    
    print("\nReducing to 2D with PCA for visualization...")
    pca = PCA(n_components=2, random_state=42)
    reduced = pca.fit_transform(tagged_matrix)

    print(f"Saving plot to '{PLOT_FILE}'...")
    cmap = plt.colormaps['tab10'].resampled(K)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for cluster_id, ax in enumerate(axes.flat):
        ax.scatter(reduced[:, 0], reduced[:, 1], c='lightgray', s=1, alpha=0.3)
        mask = labels == cluster_id
        ax.scatter(reduced[mask, 0], reduced[mask, 1], c=[cmap(cluster_id)], s=2, alpha=0.6,)
        ax.set_title(f"Cluster {cluster_id}")
    
    fig.suptitle(f"Game cluster (k={K}) -- PCA Projection")
    plt.savefig(PLOT_FILE, dpi=150)
    print("Done!")


if __name__ == "__main__":
    inspect_clusters()