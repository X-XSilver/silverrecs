import numpy as np
from num2words import num2words
from fastapi import APIRouter, Query
from .query_database import get_game_data
from .vectors_helper import create_sentence, prepare_query


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

    #sentence = f"{title} {tags}".replace( ",", "")
    sentence = create_sentence(appid, tags)
    print(f"Recs Query: {sentence}")
    
    vector_2d = prepare_query(models.ft_model, sentence)


    distance, indices = models.index.search(vector_2d, 6)

    nearest_ids = [int(idx) for idx in indices[0] if int(idx) != int(appid)][:5]

    print(f"Near Games: {nearest_ids}")

    return get_game_data(nearest_ids)
