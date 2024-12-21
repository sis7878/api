from flask import Flask
from models import db
from routes import pizza_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(pizza_bp, url_prefix='/api/pizza')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
