from flask import Blueprint, request, jsonify
import numpy as np

from app.services.data_fetcher import fetch_structured_stats
from app.services.nlp_service import scrape_news_sentiment
from app.services.odds_service import fetch_current_odds

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict", methods=["POST"])
def predict_match():
    """
    This endpoint receives match info,
    asks the AI model to think,
    and returns a prediction.
    """

    data = request.get_json()

    # --- Step 1: Validate input ---
    if not data:
        return jsonify({"error": "No data sent"}), 400

    match_id = data.get("match_id")
    home_team = data.get("home_team")
    away_team = data.get("away_team")

    if not match_id or not home_team or not away_team:
        return jsonify({"error": "Missing required fields"}), 400

    # --- Step 2: Gather features ---
    stats_df = fetch_structured_stats(match_id)
    home_nlp = scrape_news_sentiment(home_team)
    away_nlp = scrape_news_sentiment(away_team)

    # If no stats, use safe defaults
    features = {}

    if not stats_df.empty:
        features.update(stats_df.iloc[0].to_dict())

    features.update({
        "home_morale": home_nlp["morale"],
        "away_injury_impact": away_nlp["injury_impact"]
    })

    # Convert features to array (mock model for now)
    feature_vector = np.array(list(features.values())).reshape(1, -1)

    # --- Step 3: Model prediction (mocked for now) ---
    # Later we will load the real model
    prediction_probas = np.array([0.75, 0.15, 0.10])

    p_home, p_draw, p_away = prediction_probas

    # --- Step 4: Get bookmaker odds ---
    home_odds, draw_odds, away_odds = fetch_current_odds(match_id)

    # --- Step 5: Calculate value ---
    value_home = (p_home * home_odds) - 1
    value_draw = (p_draw * draw_odds) - 1
    value_away = (p_away * away_odds) - 1

    best_bet = "No Value Found"
    if max(value_home, value_draw, value_away) > 0:
        best_bet = max(
            {
                "Home Win": value_home,
                "Draw": value_draw,
                "Away Win": value_away
            },
            key=lambda x: {
                "Home Win": value_home,
                "Draw": value_draw,
                "Away Win": value_away
            }[x]
        )

    # --- Step 6: Send response ---
    return jsonify({
        "match_id": match_id,
        "home_team": home_team,
        "away_team": away_team,
        "app_probabilities": {
            "Home_Win": round(p_home, 4),
            "Draw": round(p_draw, 4),
            "Away_Win": round(p_away, 4)
        },
        "value_scores": {
            "Home_Win_Value": round(value_home, 4),
            "Draw_Value": round(value_draw, 4),
            "Away_Win_Value": round(value_away, 4)
        },
        "best_bet": best_bet
    })
