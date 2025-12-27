from flask import Blueprint, jsonify, request

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    required_fields = ["match_id", "home_team", "away_team"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Mock AI prediction (placeholder)
    prediction = {
        "home_win": 0.55,
        "draw": 0.25,
        "away_win": 0.20
    }

    result = {
        "match_id": data["match_id"],
        "home_team": data["home_team"],
        "away_team": data["away_team"],
        "prediction": prediction,
        "best_bet": "Home Win",
        "confidence": "Medium"
    }

    return jsonify(result)
