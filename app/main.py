from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # ✅ Global CORS – allow Lovable previews + production
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=False
    )

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    # Register blueprints
    from app.routes.predict import predict_bp
    from app.routes.fixtures import fixtures_bp

    app.register_blueprint(predict_bp)
    app.register_blueprint(fixtures_bp)

    return app
