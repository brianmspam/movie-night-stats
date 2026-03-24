from flask import Blueprint, render_template
from app.models import Movie, Rating, Person
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    total_movies = Movie.query.count()
    total_ratings = Rating.query.count()
    total_people = Person.query.count()
    recent_movies = Movie.query.order_by(Movie.added.desc()).limit(5).all()
    return render_template('index.html',
                           total_movies=total_movies,
                           total_ratings=total_ratings,
                           total_people=total_people,
                           recent_movies=recent_movies)