import sqlite3
import numpy as np
import os
import sys
from sklearn.cluster import KMeans

scripts_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(scripts_folder)
data_folder = os.path.join(root_folder, "data")
src_folder = os.path.join(root_folder, "src")

if src_folder not in sys.path:
    sys.path.append(src_folder)

from vectors_helper import normalize_vectors

DB_PATH = os.path.join(data_folder, "steam_games.db")
VECTORS_FILE = os.path.join(data_folder, "game_vectors.npz")

K = 6

def build_clusters():

    print("Loading game vectors into memory...")
    data = np.load(VECTORS_FILE)

    ids = data['ids']
    matrix = data['vectors']

    print("Identifying empty vectors...")
    vector_norms = np.linalg.norm(matrix, axis=1)
    has_signal = vector_norms > 0

    print("Filtering out empty vectors...")
    tagged_ids = ids[has_signal]
    tagged_matrix = normalize_vectors(matrix[has_signal]).astype('float32')

    untagged_ids = ids[~has_signal]

    print(f"Performing K-Means clustering, with a K value of {6} on filtered vector matrix...")
    kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
    tagged_labels = kmeans.fit_predict(tagged_matrix)


    print("Attaching K-Means cluster id to games in database...")
    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.cursor()

        paired_entries = [
            (int(cluster_id), int(appid)) 
            for appid, cluster_id in zip(tagged_ids, tagged_labels)
        ]

        cursor.executemany(
            "UPDATE games SET clusterid = ? WHERE appid = ?", paired_entries
        )
        conn.commit()
    
    print(f"Done. Attached cluster ids to {len(tagged_ids)} games.")


if __name__ == "__main__":
    build_clusters()