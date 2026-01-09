from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
from app.routes.fixtures import fixtures_bp
app.register_blueprint(fixtures_bp)
    # ✅ Allow all origins (safe for now)
    CORS(app)

    from app.routes.predict import predict_bp
    app.register_blueprint(predict_bp)

    @app.route("/")
    def health():
        return {"status": "ok"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
