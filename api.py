from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import (
    playercareerstats,
    playergamelog,
    commonplayerinfo,
    commonteamroster,
    teaminfocommon,
)

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/team/<int:team_id>")
def team_page(team_id):
    return render_template("team.html")


@app.route("/player/<int:player_id>")
def player_page(player_id):
    return render_template("player.html")


# ── Player endpoints ──────────────────────────────────────────────────────────

@app.route("/api/search")
def search_players():
    """Search players by name, return matching list."""
    query = request.args.get("q", "").strip()
    if not query or len(query) < 2:
        return jsonify([])

    results = players.find_players_by_full_name(query)
    if not results:
        results = players.find_players_by_last_name(query)

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
                "MIN", "PTS", "REB", "AST", "STL", "BLK",
                "FG_PCT", "FG3_PCT", "FT_PCT", "TOV"]
        df = df[[c for c in cols if c in df.columns]]
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/player/<int:player_id>/gamelog")
def player_gamelog(player_id):
    """Get game-by-game log for current season."""
    season = request.args.get("season", "2024-25")
    try:
        log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        df = log.get_data_frames()[0]
        cols = ["GAME_DATE", "MATCHUP", "WL", "MIN", "PTS", "REB", "AST",
                "STL", "BLK", "FG_PCT", "FG3M", "FTM", "TOV", "PLUS_MINUS"]
        df = df[[c for c in cols if c in df.columns]]
        return jsonify(df.head(20).to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Team endpoints ────────────────────────────────────────────────────────────

@app.route("/api/team/<int:team_id>/info")
def team_info(team_id):
    """Return basic team info (name, abbreviation, city)."""
    try:
        all_teams = teams.get_teams()
        team = next((t for t in all_teams if t["id"] == team_id), None)
        if not team:
            return jsonify({"error": "Team not found"}), 404
        return jsonify({
            "id": team["id"],
            "name": team["full_name"],
            "abbreviation": team["abbreviation"],
            "city": team["city"],
            "nickname": team["nickname"],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/team/<int:team_id>/roster")
def team_roster(team_id):
    """Return the current roster for a team, with the year each player first joined."""
    try:
        roster = commonteamroster.CommonTeamRoster(team_id=team_id)
        df = roster.get_data_frames()[0]

        # Get team abbreviation to match against career stats
        all_teams = teams.get_teams()
        team = next((t for t in all_teams if t["id"] == team_id), None)
        team_abbr = team["abbreviation"] if team else None

        players_list = []
        for _, row in df.iterrows():
            player_id = int(row.get("PLAYER_ID", 0))
            season_joined = "N/A"

            if team_abbr:
                try:
                    career = playercareerstats.PlayerCareerStats(player_id=player_id)
                    career_df = career.get_data_frames()[0]
                    # Filter to seasons with this team, find the earliest
                    team_seasons = career_df[career_df["TEAM_ABBREVIATION"] == team_abbr]
                    if not team_seasons.empty:
                        first_season = team_seasons.iloc[0]["SEASON_ID"]
                        # SEASON_ID is like "2019-20", extract the start year
                        season_joined = first_season.split("-")[0]
                except Exception:
                    pass

            players_list.append({
                "id": player_id,
                "name": row.get("PLAYER", "N/A"),
                "position": row.get("POSITION", "N/A"),
                "jersey": row.get("NUM", "N/A"),
                "season": season_joined,
            })
        return jsonify(players_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)