import sqlite3
import os



def get_game_data(faiss_row_indices, current_appid, exclude_ids):
    
    game_data = []


    src_folder = os.path.dirname(os.path.abspath(__file__))
    root_folder = os.path.dirname(src_folder)
    data_folder = os.path.join(root_folder, "data")

    data_base_path = os.path.join(data_folder, "steam_games.db")
    
   
    with sqlite3.connect(data_base_path) as conn:
        
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
                "image": game['image']
            }

            game_data.append({"id": len(game_data) + 1, "data": game_print})

            if len(game_data) == 5:
                break

    return game_data