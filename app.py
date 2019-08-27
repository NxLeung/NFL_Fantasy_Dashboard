# import necessary libraries
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine
import json
# create instance of Flask app
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def index():
    # 0. read data from database
    engine = create_engine(f"postgresql://postgres:postgres@localhost/nfl_db")
    df_player = pd.read_sql("""select * from "Player" where player_name in ('P.Manning') """, engine)
    # 1. transform every row to json
    df_player['json'] = df_player.apply(lambda x: x.to_json(), axis=1)
    # 2. combine each json as a list
    player_info_list = list(df_player['json'].unique())
    # 3. create a dict to store each json by name
    player_info_json = {}
    for play_info in player_info_list:
        play_info = dict(json.loads(play_info))
        if player_info_json.get(play_info['player_name']) == None:
            key = play_info['player_name']
            value = json.dumps(play_info)
            player_info_json[key] = value
        else:
            key = play_info['player_name']
            player_info_json[key] = player_info_json[key] + ',' + json.dumps(play_info)
    player_info_json

    return render_template("index.html", json=dict(player_info_json))
@app.route("/player_data", methods=['GET'])
def pass_data():
    if 'player_name' in request.args:
        play_name = request.args['player_name']
    else:
        play_name = 'P.Manning'
    engine = create_engine(f"postgresql://postgres:postgres@localhost/nfl_db")
    df_player = pd.read_sql(f"""select * from "Player" where player_name = '{play_name}' """, engine)
    # 1. transform every row to json
    df_player['json'] = df_player.apply(lambda x: x.to_json(), axis=1)
    # 2. combine each json as a list
    player_info_list = list(df_player['json'].unique())
    # 3. create a dict to store each json by name
    player_info_json = {}
    for play_info in player_info_list:
        play_info = dict(json.loads(play_info))
        if player_info_json.get(play_info['player_name']) == None:
            key = play_info['player_name']
            value = json.dumps(play_info)
            player_info_json[key] = value
        else:
            key = play_info['player_name']
            player_info_json[key] = player_info_json[key] + ',' + json.dumps(play_info)
    return json.dumps(player_info_json)

if __name__ == "__main__":
    app.run(debug=True)
