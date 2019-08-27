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
    df_player = pd.read_sql("""select * from "Player" where player_name = 'P.Manning' """, engine)

    df_player.fillna(0, inplace=True)
    df_player_year = df_player.groupby(["game_year"]).sum()
    df_player_year = df_player_year.reset_index()

    player_info = {}
    player_name = list(df_player.player_name.unique())[0]
    player_info[player_name] = {}

    year_list = sorted(list(df_player_year.game_year.unique()))
    for year in year_list:
        df_info = df_player[df_player.game_year == year][['passing_yards_gained', 'receiving_yards_gained', 'rushing_yards_gained']]
        df_info['json'] = df_info.apply(lambda x: x.to_json(), axis=1)

        player_info[player_name][year] = ','.join(df_info['json'].unique())

    player_info


    return render_template("index.html", json=dict(player_info))

@app.route("/player_data", methods=['GET'])
def pass_data():
    if 'player_name' in request.args:
        player_name = request.args['player_name']
    else:
        player_name = 'P.Manning'
    engine = create_engine(f"postgresql://postgres:postgres@localhost/nfl_db")
    df_player = pd.read_sql(f"""select * from "Player" where player_name = '{player_name}' """, engine)

    df_player.fillna(0, inplace=True)
    df_player_year = df_player.groupby(["game_year"]).sum()
    df_player_year = df_player_year.reset_index()

    player_info = {}
    player_name = list(df_player.player_name.unique())[0]
    player_info[player_name] = {}

    year_list = sorted(list(df_player_year.game_year.unique()))

    for year in year_list:
        df_info = df_player[df_player.game_year == year][['passing_yards_gained', 'receiving_yards_gained', 'rushing_yards_gained']]
        df_info['json'] = df_info.apply(lambda x: x.to_json(), axis=1)

        player_info[player_name][year] = ','.join(df_info['json'].unique())

    return json.dumps(player_info)

if __name__ == "__main__":
    app.run(debug=True)
