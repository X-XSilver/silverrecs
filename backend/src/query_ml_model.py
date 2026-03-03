import numpy as np
from fastapi import APIRouter, Query
from .query_database import get_game_data

router = APIRouter()

class AIModelStore:
    index = None
    ft_model = None


models = AIModelStore()


@router.get("/api/gen_recs/{appid}")
async def get_recs(
    appid: int,
    title: str = Query(...),
    tags: str = Query("")):

    sentence = f"{title} {tags}".replace( ",", "")

    vector = models.ft_model.get_sentence_vector(sentence)
    vector_2d = np.array([vector]).astype('float32')


    distance, indices = models.index.search(vector_2d, 6)

    nearest_ids = [int(idx) for idx in indices[0] if int(idx) != int(appid)][:5]


    return get_game_data(nearest_ids)
