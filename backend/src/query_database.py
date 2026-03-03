import sqlite3
import os



def get_game_data(appids):
    game_data = []
    
    placeholders = ", ".join("?" for _ in appids)

    query = f"SELECT * FROM games WHERE appid IN ({placeholders})"

    src_folder = os.path.dirname(os.path.abspath(__file__))
    root_folder = os.path.dirname(src_folder)
    data_folder = os.path.join(root_folder, "data")

    data_base_path = os.path.join(data_folder, "steam_games.db")
    
    with sqlite3.connect(data_base_path) as conn:
        
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(query, appids)
        results = [dict(row) for row in cursor.fetchall()]
        #print(results)
    i = 0
    for game in results:

        game_print = {
            "appid": game['appid'],
            "title": game['title'],
            "tags": game['tags'] if len(game['tags']) > 0 else "No Tags",
            "description": game['description'] if len(game['description']) > 0 else "No Description",
            "image": game['image']
            }

        game_data.append({"id": i+1, "data": game_print})
        i = i + 1

    return game_data