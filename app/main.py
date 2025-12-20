from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.predict import predict_bp
    app.register_blueprint(predict_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
