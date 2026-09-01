"""
Satisfies:
    - collected or available datasets
    - ability to support featurizing, parsing, cleaning, and wrangling datasets

This script takes database of games in .json format and turns it into a .db sqlite database for fast use.
The script truncates unnecassary fields and makes a light table of only what is necessary.
"""
import sqlite3
import ijson
import json
import os


scripts_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(scripts_folder)
data_folder = os.path.join(root_folder, "data")

data_base_path = os.path.join(data_folder, "steam_games.db")

conn = sqlite3.connect(data_base_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        appid INTEGER PRIMARY KEY,
        clusterid INTEGER NULL,
        title TEXT,
        description TEXT,
        tags TEXT,
        image TEXT
    )
''')

def tag_str(tags: dict) -> str:
    return json.dumps(tags) if tags else '{}'

data_set_path = os.path.join(data_folder, "games.json")

with open(data_set_path, 'r', encoding="utf8") as f:
    
    batch = []
    games_added = 0

    for app_id, item in ijson.kvitems(f, ''):
        
        batch.append((
            app_id,
            item.get('name'),
            item.get('short_description'),
            tag_str(item.get('tags')),
            item.get('header_image')
        ))

        games_added += 1

        if len(batch) >= 5000:
            cursor.executemany('INSERT OR REPLACE INTO games (appid, title, description, tags, image) VALUES (?, ?, ?, ?, ?)', batch)
            conn.commit()
            batch = []
            print(f"Added {games_added} games to sqlite database...")

    if batch:
        cursor.executemany('INSERT OR REPLACE INTO games (appid, title, description, tags, image) VALUES (?, ?, ?, ?, ?)', batch)
        conn.commit()

print(f"Done. Made an sqlite database with {games_added} games in it.")
conn.close()