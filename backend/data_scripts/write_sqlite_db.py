import sqlite3
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
        title TEXT,
        description TEXT,
        tags TEXT,
        image TEXT
    )
''')

def tag_str(tags: dict) -> str:
    string = ''

    for tag in tags:
        string += tag + ', '
    return string

data_set_path = os.path.join(root_folder, "games.json")

with open(data_set_path, 'r', encoding="utf8") as f:
    data = json.load(f)

to_insert = [
    (
        app_id,
        item.get('name'),
        item.get('short_description'),
        tag_str(item.get('tags')),
        item.get('header_image')
    )
    for app_id, item in data.items()
]

cursor.executemany(
    'INSERT OR REPLACE INTO games (appid, title, description, tags, image) VALUES (?, ?, ?, ?, ?)', 
    to_insert
)

conn.commit()
conn.close()