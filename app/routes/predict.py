from flask import Blueprint, jsonify, request

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing JSON body"
        }), 400

    required_fields = ["match_id", "home_team", "away_team"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    return jsonify({
        "status": "success",
        "received": data
    })
