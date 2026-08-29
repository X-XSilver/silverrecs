import sqlite3
import compress_fasttext
import numpy as np
import os
import sys

scripts_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(scripts_folder)
data_folder = os.path.join(root_folder, "data")
src_folder = os.path.join(root_folder, "src")

if src_folder not in sys.path:
    sys.path.append(src_folder)

from vectors_helper import create_sentence, get_sentence_vector


DB_PATH = os.path.join(data_folder, "steam_games.db")
MODEL_PATH = os.path.join(data_folder, "cc.en.300.compressed.bin")
VECTORS_FILE = os.path.join(data_folder, "game_vectors.npz")

PROGRESS_INTERVAL = 10000




def build_vectors():

    print("Loading fastText model... (this may take a moment)")
    ft_model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(MODEL_PATH)


    print("Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    rows = conn.execute("SELECT appid, tags FROM games").fetchall()
    conn.close()

    print(f"Processing {len(rows)} games...")

    id_list = []
    vector_list = []


    for appid, tags in rows:
       
        sentence = create_sentence(appid, tags)
        vector = get_sentence_vector(ft_model, sentence)


        id_list.append(appid)
        vector_list.append(vector)

        if len(id_list) % PROGRESS_INTERVAL == 0:
            
            print(f"Processed {len(id_list)} games...")
        
    print(f"Processed {len(id_list)} games total.")



    ids_np = np.array(id_list).astype('int64')
    vectors_np = np.array(vector_list).astype('float32')

    print(f"Saving vector matrix to '{VECTORS_FILE}'...")
    np.savez(VECTORS_FILE, ids=ids_np, vectors=vectors_np)
    print("Done!")


if __name__ == "__main__":
    build_vectors()