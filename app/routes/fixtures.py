from flask import Blueprint, jsonify, request
import requests
import os

fixtures_bp = Blueprint("fixtures", __name__)

@fixtures_bp.route("/fixtures", methods=["GET"])
def fixtures():
    sport = request.args.get("sport") or request.args.get("sportId")

    if not sport:
        return jsonify({
            "success": False,
            "error": "Sport is required",
            "fixtures": []
        })

    API_KEY = os.environ.get("ODDS_API_KEY")

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "eu",
        "markets": "h2h"
    }

    res = requests.get(url, params=params)
    data = res.json()

    return jsonify({
        "success": True,
        "fixtures": data
    })
