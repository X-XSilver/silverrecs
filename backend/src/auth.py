"""
Satisfies:
    - industry-appropriate security features

This script completes the authentication handshake between the Steam API
and the app to allow for user's to login to their Steam account.
It uses a JWT Token for further security standards. This HS256 token
is an industry standard authentication artifact.
"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from jose import jwt
from datetime import datetime, timedelta
from urllib.parse import urlparse
import requests
import os

router = APIRouter()


STEAM_VERIFY_URL = "https://steamcommunity.com/openid/login"
ALGO = "HS256"
DEV_MODE = os.environ.get("DEV_MODE", "false").lower() == "true"


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

    if DEV_MODE:
        print("DEV_MODE active - skipping real Steam verification.")
        is_valid = True
    else:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://steamcommunity.com',
            'Referer': 'https://steamcommunity.com/openid/login'
        }

        response = requests.post(STEAM_VERIFY_URL, data=verify_query, headers=headers)
        is_valid = "is_valid:true" in response.text

    if not is_valid:
        raise HTTPException(status_code=400, detail="Steam authentication failed")

    steam_id = request.query_params.get("openid.claimed_id").split("/")[-1]

    token = create_access_token(steam_id)

    frontend_base = request.query_params.get("fr")

    if not frontend_base:

        forwarded_host = request.headers.get("x-forwarded-host") or request.headers.get("host")


        scheme = request.headers.get("x-forwarded-proto", "https")
        if "localhost" in str(forwarded_host) or "127.0.0.1" in str(forwarded_host):
            scheme = "http"
    
        frontend_base = f"{scheme}://{forwarded_host}" if forwarded_host else "https://silverrecs.com"
    
    
    return_point_url = f"{frontend_base}/#/verify_steam?token={token}"

    return RedirectResponse(url=return_point_url, status_code=302)