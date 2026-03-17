from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, playergamelog, commonplayerinfo

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/search")
def search_players():
    """Search players by name, return matching list."""
    query = request.args.get("q", "").strip()
    if not query or len(query) < 2:
        return jsonify([])

    results = players.find_players_by_full_name(query)
    # Also search by last name
    if not results:
        results = players.find_players_by_last_name(query)

    # Return top 8 matches with basic info
    simplified = [
        {"id": p["id"], "name": p["full_name"], "active": p["is_active"]}
        for p in results[:8]
    ]
    return jsonify(simplified)


@app.route("/api/player/<int:player_id>/info")
def player_info(player_id):
    try:
        info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        df = info.get_data_frames()[0]
        data = df.iloc[0].to_dict()
        data = {k: (int(v) if hasattr(v, 'item') else v) for k, v in data.items()}
        return jsonify({
            "name": data.get("DISPLAY_FIRST_LAST") or data.get("PLAYER_NAME", "N/A"),
            "team": data.get("TEAM_NAME", "N/A"),
            "position": data.get("POSITION", "N/A"),
            "jersey": data.get("JERSEY", "N/A"),
            "height": data.get("HEIGHT", "N/A"),
            "weight": data.get("WEIGHT", "N/A"),
            "country": data.get("COUNTRY", "N/A"),
            "experience": data.get("SEASON_EXP", "N/A"),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/player/<int:player_id>/career")
def player_career(player_id):
    """Get full career stats per season."""
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        df = career.get_data_frames()[0]
        cols = ["SEASON_ID", "TEAM_ABBREVIATION", "GP", "GS",
                "MIN", "PTS", "REB", "AST", "STL", "BLK", "FG_PCT", "FG3_PCT", "FT_PCT", "TOV"]
        df = df[[c for c in cols if c in df.columns]]
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/player/<int:player_id>/gamelog")
def player_gamelog(player_id):
    """Get game-by-game log for current season."""
    season = request.args.get("season", "2023-24")
    try:
        log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        df = log.get_data_frames()[0]
        cols = ["GAME_DATE", "MATCHUP", "WL", "MIN", "PTS", "REB", "AST", "STL", "BLK", "FG_PCT", "FG3M", "FTM", "TOV", "PLUS_MINUS"]
        df = df[[c for c in cols if c in df.columns]]
        return jsonify(df.head(20).to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)