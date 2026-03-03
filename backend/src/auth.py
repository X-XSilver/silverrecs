from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from jose import jwt
from datetime import datetime, timedelta
import requests
import os

router = APIRouter()


STEAM_VERIFY_URL = "https://steamcommunity.com/openid/login"
ALGO = "HS256"



def create_access_token(steam_id: str):

    secret_key = os.environ.get("JWT_SECRET_KEY")

    if not secret_key:
        raise ValueError("Missing JWT_SECRET_KEY environment variable!")
    
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"sub": steam_id, "exp": expire}
    return jwt.encode(to_encode, secret_key, algorithm=ALGO)


@router.get("/api/auth/steam_login")
async def verify_steam(request: Request):

    raw_query = str(request.query_params)

    verify_query = raw_query.replace("openid.mode=id_res", "openid.mode=check_authentication")

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(STEAM_VERIFY_URL, data=verify_query, headers=headers)

    if "is_valid:true" not in response.text:
        raise HTTPException(status_code=400, detail="Steam authentication failed")

    steam_id = request.query_params.get("openid.claimed_id").split("/")[-1]

    token = create_access_token(steam_id)

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost")
    
    return_point_url = f"{frontend_url}/#/verify_steam?token={token}"

    return RedirectResponse(url=return_point_url)