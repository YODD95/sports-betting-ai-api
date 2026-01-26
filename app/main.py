from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={r"/*": {
            "origins": [
                "https://lovable.dev",
                "https://*.lovable.app"
            ]
        }},
        supports_credentials=True
    )

    @app.route("/health")
    def health():
        return {"status": "ok"}

    from app.routes.predict import predict_bp
    app.register_blueprint(predict_bp)

    from app.routes.fixtures import fixtures_bp
    app.register_blueprint(fixtures_bp)

    return app


# REQUIRED for Gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
