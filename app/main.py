from flask import Flask

def create_app():
    app = Flask(__name__)

    # 🔵 HEALTH CHECK (MUST BE INSIDE THE FACTORY)
    @app.route("/health")
    def health():
        return {"status": "ok"}

    from app.routes.predict import predict_bp
    app.register_blueprint(predict_bp)

    return app

# 🔴 GUNICORN NEEDS THIS
app = create_app()

# 🔵 LOCAL DEV ONLY
if __name__ == "__main__":
    app.run(debug=True)
