from flask import Blueprint, jsonify, request
import requests
import os

fixtures_bp = Blueprint("fixtures", __name__)

# 🔁 Map frontend sport names → Odds API sport keys
SPORT_MAP = {
    "football": "soccer_epl",          # English Premier League
    "basketball": "basketball_nba",
    "tennis": "tennis_atp",
    "cricket": "cricket_international",
    "mma": "mma_mixed_martial_arts"
}

@fixtures_bp.route("/fixtures", methods=["GET"])
def fixtures():
    sport = request.args.get("sport")

    if not sport:
        return jsonify({
            "success": False,
            "error": "Sport is required",
            "fixtures": []
        }), 400

    # Translate sport → Odds API key
    odds_sport = SPORT_MAP.get(sport)

    if not odds_sport:
        return jsonify({
            "success": False,
            "error": f"Unsupported sport: {sport}",
            "fixtures": []
        }), 400

    API_KEY = os.environ.get("ODDS_API_KEY")

    if not API_KEY:
        return jsonify({
            "success": False,
            "error": "ODDS_API_KEY missing",
            "fixtures": []
        }), 500

    url = f"https://api.the-odds-api.com/v4/sports/{odds_sport}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": "eu",
        "markets": "h2h"
    }

    res = requests.get(url, params=params)

    if res.status_code != 200:
        return jsonify({
            "success": False,
            "error": f"Odds API error {res.status_code}",
            "fixtures": []
        }), 400

    data = res.json()

    return jsonify({
        "success": True,
        "count": len(data),
        "fixtures": data
    })
