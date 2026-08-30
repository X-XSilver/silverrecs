import json
import numpy as np
from num2words import num2words



def create_sentence(appid, tags):
    safe_game_id = f"gameid{num2words(appid)}" if appid else ""
    safe_tags = tags if tags else ""
    return f"{safe_game_id} {safe_tags}".replace("\n", " ").strip()


def get_sentence_vector(model, tags_str):
    
    try:
        tags_dict = json.loads(tags_str)
    except:
        return np.zeros(model.vector_size)

    if not isinstance(tags_dict, dict):
        return np.zeros(model.vector_size)

    
    tag_vecs = []
    weights = []

    for tag, count in tags_dict.items():

        words = tag.split()
        word_vecs = [model[w] for w in words if w in model]

        if not word_vecs:
            continue
        
        tag_vec = np.mean(word_vecs, axis=0)
        tag_vecs.append(tag_vec)

        try: 
            weight = np.log1p(float(count))
        except (TypeError, ValueError):
            continue
        
        weights.append(weight)
    
    if not tag_vecs or not weights or len(tag_vecs) != len(weights):
        return np.zeros(model.vector_size)
    
    tag_vecs = np.array(tag_vecs)
    weights = np.array(weights, dtype='float32')

    
    
    return np.average(tag_vecs, axis=0, weights=weights)


def normalize_vectors(vectors_np):

    norms = np.linalg.norm(vectors_np, axis=1, keepdims=True)
    norms[norms==0] = 1.0
    return vectors_np / norms

def prepare_query(model, tags_str):
    
    vec = get_sentence_vector(model, tags_str)
    matrix = np.array([vec], dtype=np.float32)

    return normalize_vectors(matrix)