from flask import Blueprint, request, jsonify
import numpy as np

from app.services.data_fetcher import fetch_structured_stats, fetch_current_odds
from app.services.nlp_service import scrape_news_sentiment
from app.services.model_service import load_model, predict_probabilities

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")

MODEL = load_model()

@predict_bp.route("", methods=["POST"])
def predict():
    data = request.json

    match_id = data.get("match_id")
    home_team = data.get("home_team")
    away_team = data.get("away_team")

    if not match_id:
        return jsonify({"error": "match_id is required"}), 400

    stats_df = fetch_structured_stats(match_id)

    home_nlp = scrape_news_sentiment(home_team)
    away_nlp = scrape_news_sentiment(away_team)

    features = {}

    if not stats_df.empty:
        features.update(stats_df.iloc[0].to_dict())

    features.update({
        "home_morale": home_nlp["morale"],
        "away_injury_impact": away_nlp["injury_impact"]
    })

    feature_vector = np.array(list(features.values())).reshape(1, -1)

    probabilities = predict_probabilities(MODEL, feature_vector)

    home_odds, draw_odds, away_odds = fetch_current_odds(match_id)

    result = {
        "probabilities": probabilities,
        "odds": {
            "home": home_odds,
            "draw": draw_odds,
            "away": away_odds
        }
    }

    return jsonify(result)
# Prediction routes
