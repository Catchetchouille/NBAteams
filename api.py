from flask import Flask, jsonify
from flask_cors import CORS
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

app = Flask(__name__)
CORS(app)

@app.route("/api/lebron")
def lebron_stats():
    # Find player
    player_dict = players.find_players_by_full_name('LeBron James')
    player_id = player_dict[0]['id']

    # Get career stats
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career.get_data_frames()[0]

    # Convert dataframe to JSON
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)