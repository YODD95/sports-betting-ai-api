from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def health():
        return jsonify({"status": "ok"})

    from app.routes.predict import predict_bp
    from app.routes.fixtures import fixtures_bp

    app.register_blueprint(predict_bp)
    app.register_blueprint(fixtures_bp)

    return app

# 👇 THIS LINE IS WHAT GUNICORN NEEDS
app = create_app()
