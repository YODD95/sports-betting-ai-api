from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # ✅ CORS — allow Lovable + browser access
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers="*",
        methods=["GET", "POST", "OPTIONS"],
    )

    # ✅ Health check (used by Render)
    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok"}

    # ✅ Register blueprints
    from app.routes.predict import predict_bp
    from app.routes.fixtures import fixtures_bp

    app.register_blueprint(predict_bp)
    app.register_blueprint(fixtures_bp)

    return app
