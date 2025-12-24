from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.predict import predict_bp
    app.register_blueprint(predict_bp)

    return app

# 🔴 THIS LINE IS REQUIRED FOR GUNICORN
app = create_app()

# 🔵 This block is ONLY for local testing
if __name__ == "__main__":
    app.run(debug=True)

