# import necessary libraries
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient
from config import api_key
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import json
import copy
from flask_cors import CORS
# create instance of Flask app
app = Flask(__name__)
CORS(app)
# Initialize news client
api = NewsApiClient(api_key=api_key)

# create route that renders index.html template
@app.route("/")
def index():
    # 0. read data from database
    engine = create_engine(f"postgresql://postgres:postgres@localhost/NFL")
    df_player = pd.read_sql("""select * from "Player" where player_name = 'P.Manning' """, engine)

    df_player.fillna(0, inplace=True)
    df_player = df_player.astype({"game_year": int})
    df_player_year = df_player.drop(columns=['play_type'])
    df_player_year = df_player_year.groupby(["player_id","player_name","game_year"]).sum()
    df_player_year = df_player_year.reset_index()

    player_info = {}
    player_name = list(df_player_year.player_name.unique())[0]
    player_info[player_name] = {}

    year_list = sorted(list(df_player_year.game_year.unique()))
    for year in year_list:
        df_info = df_player_year[df_player_year.game_year == year][['passing_yards_gained', 'receiving_yards_gained', 'rushing_yards_gained']]
        df_info['json'] = df_info.apply(lambda x: x.to_json(), axis=1)
        
    #     player_info[player_name][year] = ','.join(df_info['json'].unique())
        player_info[player_name][year] = list(df_info['json'].unique())[0]
    player_info

    return render_template("index.html", json=dict(player_info))


@app.route('/data/<selectedOption>')
def playerData (selectedOption):
    player_name = selectedOption;
    engine = create_engine(f"postgresql://postgres:postgres@localhost/NFL")
    conn = engine.connect()
    playerData = pd.read_sql(f"""select game_year, sum(passing_yards_gained) as passing_yards_gained,sum(receiving_yards_gained) as receiving_yards_gained,sum(rushing_yards_gained) as rushing_yards_gained
FROM
	"Player" where player_name = '{player_name}' group by game_year """, engine)
    playerData.fillna(0, inplace=True)
    playerData = playerData.to_json(orient='records')
 
    return playerData
 



@app.route('/linchart', methods=['GET'])
def line_chart():
    # # STEP 1: API Receive play_name as a value, default is 'P,Manning'
    # if 'player_name' in request.args:
    #     player_name = request.args['player_name']
    # else:
    #     player_name = 'P.Manning'
    # # STEP 2: Query Player Data from DB, based on the api received value    
    # engine = create_engine(f"postgresql://postgres:postgres@localhost/nfl")
    # df_player = pd.read_sql(f"""select * from "Player" where player_name = '{player_name}' """, engine)
    # # STEP 2.2: if nothing return, return 
    # if len(df_player) == 0:
    #     return json.dumps({'error_msg':'player not found!'})
    # # STEP 3: Transform Data
    # # STEP 3.1: clean data & group by 
    # df_player.fillna(0, inplace=True)
    # df_player = df_player.astype({"game_year": int})
    # df_player_year = df_player.drop(columns=['play_type'])
    # df_player_year = df_player_year.groupby(["player_id","player_name","game_year"]).sum()
    # df_player_year = df_player_year.reset_index()
    # # STEP 3.2: turn dataframe to dictionary
    # player_info = {}
    # player_name = list(df_player_year.player_name.unique())[0]
    # player_info[player_name] = {}

    # year_list = sorted(list(df_player_year.game_year.unique()))
    # # result = []
    # # STEP 3.3: extract data by year
    # # for year in year_list:
    # #     # 3.3.1. select by year
    # #     df_info = df_player_year[df_player_year.game_year == year][['passing_yards_gained', 'receiving_yards_gained', 'rushing_yards_gained']]
    # #     # 3.3.2. transfrom each to dict
    # #     df_info['json'] = df_info.apply(lambda x: x.to_dict(), axis=1)
    # #     # 3.3.3. create key, value pair dictionary
    # #     cur_data = {**list(df_info['json'])[0], **{'game_year': year}}
    # #     # prev_data = copy.deepcopy(player_info[player_name])
    # #     # print(cur_data, player_info[player_name])
    # #     result.append(cur_data)
    # year_list = list(df_player_year.game_year.unique())
    # passing = list(df_player_year.passing_yards_gained.unique())
    # receiving = list(df_player_year.receiving_yards_gained.unique())
    # rushing = list(df_player_year.rushing_yards_gained.unique())

    # player_info[player_name] = {'game_year': year_list,
    #                             'passing_yards_gained': passing,
    #                             'receiving_yards_gained': receiving,
    #                             'rushing_yards_gained': rushing}
    # print(player_info[player_name])
    
    # # STEP 4. Turn dictionary to json for frontend to use
    # data = player_info
    return render_template('linechart.html') 


@app.route("/player_data", methods=['GET'])
def pass_data():
    # STEP 1: API Receive play_name as a value, default is 'P,Manning'
    if 'player_name' in request.args:
        player_name = request.args['player_name']
    else:
        player_name = 'P.Manning'
    # STEP 2: Query Player Data from DB, based on the api received value    
    engine = create_engine(f"postgresql://postgres:postgres@localhost/NFL")
    df_player = pd.read_sql(f"""select * from "Player" where player_name = '{player_name}' """, engine)
    # STEP 2.2: if nothing return, return 
    if len(df_player) == 0:
        return json.dumps({'error_msg':'player not found!'})
    # STEP 3: Transform Data
    # STEP 3.1: clean data & group by 
    df_player.fillna(0, inplace=True)
    df_player = df_player.astype({"game_year": int})
    df_player_year = df_player.drop(columns=['play_type'])
    df_player_year = df_player_year.groupby(["player_id","player_name","game_year"]).sum()
    df_player_year = df_player_year.reset_index()
    # STEP 3.2: turn dataframe to dictionary
    player_info = {}
    player_name = list(df_player_year.player_name.unique())[0]
    player_info[player_name] = {}

    year_list = sorted(list(df_player_year.game_year.unique()))
    # result = []
    # STEP 3.3: extract data by year
    # for year in year_list:
    #     # 3.3.1. select by year
    #     df_info = df_player_year[df_player_year.game_year == year][['passing_yards_gained', 'receiving_yards_gained', 'rushing_yards_gained']]
    #     # 3.3.2. transfrom each to dict
    #     df_info['json'] = df_info.apply(lambda x: x.to_dict(), axis=1)
    #     # 3.3.3. create key, value pair dictionary
    #     cur_data = {**list(df_info['json'])[0], **{'game_year': year}}
    #     # prev_data = copy.deepcopy(player_info[player_name])
    #     # print(cur_data, player_info[player_name])
    #     result.append(cur_data)

    # player_info[player_name] = result
    year_list = list(df_player_year.game_year)
    passing = list(df_player_year.passing_yards_gained)
    receiving = list(df_player_year.receiving_yards_gained)
    rushing = list(df_player_year.rushing_yards_gained)

    player_info[player_name] = {'game_year': year_list,
                                'passing_yards_gained': passing,
                                'receiving_yards_gained': receiving,
                                'rushing_yards_gained': rushing}
    print(player_info[player_name])
    # print(player_info[player_name])
    
    # STEP 4. Turn dictionary to json for frontend to use
    data = json.dumps(player_info)
    return data

if __name__ == "__main__":
    app.run(debug=True)