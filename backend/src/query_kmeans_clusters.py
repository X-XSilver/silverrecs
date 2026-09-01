"""
Satisfies:
    - one descriptive method
    - decision support functionality
    - implementation of interactive queries

This script acts as a backend endpoint for cluster exploration 
"""
from fastapi import APIRouter
from typing import Optional 
from .query_database import get_cluster_peers

router = APIRouter()


@router.get("/api/explore_cluster/{appid}")
async def explore_cluster(appid: int, exclude: Optional[str] = None):

    exclude_ids = []

    if exclude:
        exclude_ids = [int(x) for x in exclude.split(",") if x.isdigit()]
    
    cluster_games = get_cluster_peers(appid, exclude_ids)

    return cluster_games