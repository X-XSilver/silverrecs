"""
Satisfies:
    - one nondescriptive (prescriptive) method
    - implementation of interactive queries
    - implementation of machine-learning methods and algorithms
    - functionalities to evaluate the accuracy of the data product

This script takes the user given query about a specific game and
returns the 5 most similar games to the frontend. The similarity
score is also passed for recording the accuracy of the recommendations.
The similarity is determined using faiss, a similarity search library.
"""
import numpy as np
from num2words import num2words
from fastapi import APIRouter, Query
from typing import Optional
from .query_database import get_game_data
from .vectors_helper import prepare_query


router = APIRouter()

class AIModelStore:
    index = None
    ft_model = None


models = AIModelStore()


@router.get("/api/gen_recs/{appid}")
async def get_recs(
    appid: int,
    title: str = Query(...),
    tags: str = Query(""),
    exclude: Optional[str] = None):

    exclude_ids = []

    if exclude:
        exclude_ids = [int(x) for x in exclude.split(",") if x.isdigit()]
    

    vector_2d = prepare_query(models.ft_model, tags)

    distances, indices = models.index.search(vector_2d, 50)

    all_nearest_row_indices = [int(idx) for idx in indices[0]]
    scores = {int(idx): float(dist) for idx, dist in zip(indices[0], distances[0])}

    print(f"Scanning 50 FAISS positions for fresh matches...")

    fresh_recs = get_game_data(all_nearest_row_indices, appid, exclude_ids, scores)

    return fresh_recs
