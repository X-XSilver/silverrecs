#import json
import sqlite3
import os

#from .query_steam import format_tags

src_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(src_folder)
data_folder = os.path.join(root_folder, "data")

DB_PATH = os.path.join(data_folder, "steam_games.db")


def get_game_data(faiss_row_indices, current_appid, exclude_ids, scores=None):
    
    game_data = []
    
   
    with sqlite3.connect(DB_PATH) as conn:
        
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        for row_index in faiss_row_indices:

            cursor.execute("SELECT * FROM games WHERE appid = ?", (row_index,))
            row = cursor.fetchone()

            if not row:
                continue
            
            game = dict(row)
            fetched_appid= game['appid']


            if fetched_appid == current_appid:
                continue
            
            if fetched_appid in exclude_ids:
                print(f"Skipping seen game {game['title']}")
                continue

            game_print = {
                "appid": game['appid'],
                "title": game['title'],
                "tags": game['tags'] if len(game['tags']) > 0 else "No Tags",
                "description": game['description'] if len(game['description']) > 0 else "No Description",
                "image": game['image'],
                "similarity": round(scores[fetched_appid], 4) if scores and fetched_appid in scores else None
            }

            game_data.append({"id": len(game_data) + 1, "data": game_print})

            if len(game_data) == 5:
                break

    return game_data


def get_cluster_peers(appid, exclude_ids, limit=5):

    game_data = []

    with sqlite3.connect(DB_PATH) as conn:

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT clusterid FROM games WHERE appid = ?", (appid,))
        row = cursor.fetchone()

        if not row:
            return game_data
        
        cluster_id = row['clusterid']
        exclude_all = exclude_ids + [appid]
        placeholders = ",".join("?" for _ in exclude_all)

        if cluster_id is None:

            query = f"""
                SELECT * FROM games
                WHERE clusterid IS NULL AND appid NOT IN ({placeholders})
                ORDER BY RANDOM()
                LIMIT ?
            """

            params = (*exclude_all, limit)

        else:

            query = f"""
                SELECT * FROM games
                WHERE clusterid = ? AND appid NOT IN ({placeholders})
                ORDER BY RANDOM()
                LIMIT ?
            """

            params = (cluster_id, *exclude_all, limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()

        for row in rows:
            
            game = dict(row)

            game_print = {
                "appid": game['appid'],
                "title": game['title'],
                "tags": game['tags'] if len(game['tags']) > 0 else "No Tags",
                "description": game['description'] if len(game['description']) > 0 else "No Description",
                "image": game['image']
            }

            game_data.append({"id": len(game_data) + 1, "data": game_print})
    
    return game_data