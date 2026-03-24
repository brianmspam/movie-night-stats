from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Movie, Rating, Person
from app import db
from datetime import date

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/')
def list_movies():
    query = request.args.get('q', '')
    if query:
        movies = Movie.query.filter(Movie.title.ilike(f'%{query}%')).order_by(Movie.watched_on.desc()).all()
    else:
        movies = Movie.query.order_by(Movie.watched_on.desc()).all()
    return render_template('movies/list.html', movies=movies, query=query)

@movies_bp.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        year = request.form.get('year') or None
        genre = request.form.get('genre', '').strip() or None
        watched_on = request.form.get('watched_on') or None
        if not title:
            flash('Title is required.', 'error')
            return redirect(url_for('movies.add_movie'))
        movie = Movie(title=title, year=year, genre=genre, watched_on=watched_on)
        db.session.add(movie)
        db.session.commit()
        flash(f'"{title}" added!', 'success')
        return redirect(url_for('movies.detail', movie_id=movie.id))
    return render_template('movies/add.html')

@movies_bp.route('/<int:movie_id>')
def detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    people = Person.query.all()
    rated_ids = {r.person_id for r in movie.ratings}
    return render_template('movies/detail.html', movie=movie, people=people, rated_ids=rated_ids)