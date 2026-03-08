import sqlite3
import compress_fasttext
import numpy as np
import faiss
import os

scripts_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(scripts_folder)
data_folder = os.path.join(root_folder, "data")

DB_PATH = os.path.join(data_folder, "steam_games.db")
MODEL_PATH = os.path.join(data_folder, "cc.en.300.compressed.bin")
INDEX_FILE = os.path.join(data_folder, "game_index.bin")
VECTOR_DIM = 300


def build_index():

    print("Loading fastText model... (this may take a moment)")
    ft_model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(MODEL_PATH)


    print("Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    rows = conn.execute("SELECT appid, title, tags FROM games").fetchall()


    print(f"Processing {len(rows)} games...")

    quantizer = faiss.IndexFlatL2(VECTOR_DIM)
    index = faiss.IndexIDMap(quantizer)

    id_buffer = []
    vector_buffer = []

    batch_size = 10000


    for appid, title, tags in rows:
        
        safe_title = title if title else ""
        safe_tags = tags if tags else ""
        sentence = f"{safe_title} {safe_tags}".replace("\n", " ").strip()

        vector = get_sentence_vector(ft_model, sentence)


        id_buffer.append(appid)
        vector_buffer.append(vector)

        if len(id_buffer) >= batch_size:
            add_batch(index, id_buffer, vector_buffer)
            id_buffer = []
            vector_buffer = []
            print(f"Indexed {index.ntotal} games...")
        
    if id_buffer:
        add_batch(index, id_buffer, vector_buffer)

    
    print(f"Saving index with {index.ntotal} vectors to '{INDEX_FILE}'...")
    faiss.write_index(index, INDEX_FILE)
    print("Done! You can now load this file in your FastAPI app.")
    conn.close()


def add_batch(index, ids, vectors):

    ids_np = np.array(ids).astype('int64')
    vectors_np = np.array(vectors).astype('float32')

    index.add_with_ids(vectors_np, ids_np)

def get_sentence_vector(model, text):
    
    words = text.split()

    word_vecs = [model[word] for word in words if word in model]

    if not word_vecs:
        return np.zeros(model.vector_size)
    
    return np.mean(word_vecs, axis=0)

if __name__ == "__main__":
    build_index()