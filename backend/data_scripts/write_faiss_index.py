import numpy as np
import faiss
import os
import sys

scripts_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(scripts_folder)
data_folder = os.path.join(root_folder, "data")
src_folder = os.path.join(root_folder, "src")

if src_folder not in sys.path:
    sys.path.append(src_folder)

from vectors_helper import normalize_vectors


VECTORS_FILE = os.path.join(data_folder, "game_vectors.npz")
INDEX_FILE = os.path.join(data_folder, "game_index.bin")

VECTOR_DIM = 300

def build_index():

    print("Loading game vectors into memory...")
    matrix = np.load(VECTORS_FILE)

    ids_np = matrix['ids']
    vectors_np = matrix['vectors']

    print("Normalizing game vectors...")
    normalized_vectors = normalize_vectors(vectors_np).astype('float32')

    print("Building FAISS vector index...")
    quantizer = faiss.IndexFlatIP(VECTOR_DIM) #
    index = faiss.IndexIDMap(quantizer)
    index.add_with_ids(normalized_vectors, ids_np)
    print(f"Added {index.ntotal} vectors to index.")

    print(f"Writing index to '{INDEX_FILE}'...")
    faiss.write_index(index, INDEX_FILE)
    print("Done!")


if __name__ == "__main__":
    build_index()