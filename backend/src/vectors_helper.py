import numpy as np
from num2words import num2words



def create_sentence(appid, tags):
    safe_game_id = f"gameid{num2words(appid)}" if appid else ""
    safe_tags = tags if tags else ""
    return f"{safe_game_id} {safe_tags}".replace("\n", " ").strip()


def get_sentence_vector(model, text):
    
    words = text.split()

    word_vecs = [model[word] for word in words if word in model]

    if not word_vecs:
        return np.zeros(model.vector_size)
    
    return np.mean(word_vecs, axis=0)


def normalize_vectors(vectors_np):

    norms = np.linalg.norm(vectors_np, axis=1, keepdims=True)
    norms[norms==0] = 1.0
    return vectors_np / norms

def prepare_query(model, sentence):
    
    vec = get_sentence_vector(model, sentence)
    matrix = np.array([vec], dtype=np.float32)

    return normalize_vectors(matrix)