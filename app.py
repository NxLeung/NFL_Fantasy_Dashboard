# import necessary libraries
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine

# create instance of Flask app
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def index():
    # 1. Link to DB
    engine = create_engine(f"postgresql://postgres:postgres@localhost/nfl_db")
    # 2. Query Table
    df_player = pd.read_sql("""select * from "Player" where player_id = '00-0010346' """, engine)
    # 3. Data Transformation
    # 3. to Json
    player_data = df_player.to_dict()
    print(player_data)

    return render_template("index.html", dict=player_data)

if __name__ == "__main__":
    app.run(debug=True)
