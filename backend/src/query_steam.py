import requests
import json
import httpx
import os
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

def get_owned_games(api_key, steam_id):

    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"

    params = {
        'key': api_key,
        'steamid': steam_id,
        'include_appinfo': 1,
        'format': 'json'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['response'].get('games', [])
    else:
        print(f"Error: {response.status_code}")
        return []


def get_title(appid):


    url = "https://steamspy.com/api.php"

    params = {
        "request": "appdetails",
        "appid": appid
    }

    response = requests.get(url, params=params)
        
    if response.status_code == 200:
        data = response.json()

        title = data.get('name', "")

        if not title:
            return ""

        return title
    
    return None


def get_tags(appid):


    url = "https://steamspy.com/api.php"

    params = {
        "request": "appdetails",
        "appid": appid
    }

    response = requests.get(url, params=params)
        
    if response.status_code == 200:
        data = response.json()

        tags = data.get('tags', {})

        return json.dumps(tags) if tags else '{}'
    
    return None


def get_description(appid):

    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"

    

    response = requests.get(url)
    
    id_str = str(appid)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        description = "How?"

        if id_str in data and data[id_str].get("success"):
            description = data[id_str]["data"].get("short_description", "No description found")

        if not description:
            return "Failed :("
    
        return description
    else:
        print(f"Error, got following status code: {response.status_code}")


@router.get("/api/game-cover/{appid}")
async def get_image(appid):


    url = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"

    async def stream_image():

        timeout = httpx.Timeout(10.0, connect=5.0)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:

            try:
                async with client.stream("GET", url) as response:
                    if response.status_code != 200:

                        return
                    
                    async for chunk in response.aiter_bytes():
                        yield chunk
            except httpx.RequestError as e:
                print(f"Steam connection failed: {e}")

    return StreamingResponse(stream_image(), media_type="image/jpeg")


def get_game_data(appids):
    game_data = []

    api_url = os.environ.get("API_URL")

    for i in range(0, len(appids)):
        
        appid = appids[i]

        game_print = {
            "appid": appid,
            "title": get_title(appid),
            "tags": get_tags(appid),
            "description": get_description(appid),
            "image": f"{api_url}/api/game-cover/{appid}"
            }

        game_data.append({"id": i+1, "data": game_print})

    return game_data


@router.get("/api/load_user/{steam_id}")
def send_library_data(steam_id):

    api_key = os.environ.get("STEAM_API_KEY")

    if not api_key:
        raise ValueError("Missing STEAM_API_KEY environment variable!")
    games = get_owned_games(api_key, steam_id)

    sorted_games = sorted(games, key=lambda x: x['playtime_forever'], reverse=True)
    
    sorted_games = sorted_games[:5]

    appids = [game['appid'] for game in sorted_games]

    return get_game_data(appids)