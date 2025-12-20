from flask import Blueprint, jsonify, request

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    return jsonify({
        "status": "success",
        "received": data
    })
