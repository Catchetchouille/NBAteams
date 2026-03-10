from flask import Flask, render_template, request
from nba_api.stats.endpoints import playergamelog

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("test.html")

@app.route("/process", methods=["POST"])
def process():
    player_id = request.form["user_input"]

    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season="2023-24")
    df = gamelog.get_data_frames()[0]

    return render_template("test.html", result=df.to_html())

if __name__ == "__main__":
    app.run(debug=True)