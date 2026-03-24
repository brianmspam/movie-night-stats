from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'postgresql://movienight:movienight@movie_db:5432/movienightdb'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints ONLY inside this function
    from app.routes.main import main_bp
    from app.routes.movies import movies_bp
    from app.routes.people import people_bp
    from app.routes.ratings import ratings_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(movies_bp, url_prefix='/movies')
    app.register_blueprint(people_bp, url_prefix='/people')
    app.register_blueprint(ratings_bp, url_prefix='/ratings')

    return app