from flask import Blueprint, jsonify, request
import requests
import os

fixtures_bp = Blueprint("fixtures", __name__)

# 🔑 Map frontend sport names to Odds API sport keys
SPORT_MAP = {
    "football": "soccer_epl",
    "basketball": "basketball_nba",
    "tennis": "tennis_atp_aus_open",
    "cricket": "cricket_international",
    "mma": "mma_mixed_martial_arts"
}

@fixtures_bp.route("/fixtures", methods=["GET"])
def fixtures():
    frontend_sport = request.args.get("sport")

    if not frontend_sport:
        return jsonify({
            "success": False,
            "error": "Sport is required",
            "fixtures": []
        }), 400

    sport_key = SPORT_MAP.get(frontend_sport.lower())

    if not sport_key:
        return jsonify({
            "success": False,
            "error": f"Unsupported sport: {frontend_sport}",
            "fixtures": []
        }), 400

    API_KEY = os.environ.get("ODDS_API_KEY")

    if not API_KEY:
        return jsonify({
            "success": False,
            "error": "ODDS_API_KEY missing",
            "fixtures": []
        }), 500

    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Handle Odds API errors cleanly
    if isinstance(data, dict) and data.get("error_code"):
        return jsonify({
            "success": False,
            "error": data.get("message", "Odds API error"),
            "fixtures": []
        }), 400

    return jsonify({
        "success": True,
        "count": len(data),
        "fixtures": data
    })
