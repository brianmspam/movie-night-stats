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

@bp.route("/movies/add", methods=["GET", "POST"])
def add_movie():
    form = MovieForm()

    if "fetch_imdb" in request.form and form.imdb_url.data:
        try:
            data = fetch_movie_from_imdb_url_tmdb(form.imdb_url.data)
            form.title.data = data["title"]
            form.year.data = data["year"]
            form.genre.data = data["genre"]
            flash("Movie details loaded from TMDb.", "success")
        except TMDBError as e:
            flash(f"Could not load from TMDb: {e}", "danger")
        return render_template("movies/add.html", form=form)

    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            year=form.year.data,
            genre=form.genre.data,
            imdb_link=form.imdb_url.data or None,
            imdb_id=imdb_url_to_imdb_id(form.imdb_url.data) if form.imdb_url.data else None,
            tmdb_id=request.form.get("tmdb_id"),  # or add hidden field if you want
        )
        db.session.add(movie)
        db.session.commit()
        flash("Movie added.", "success")
        return redirect(url_for("main.index"))

    return render_template("movies/add.html", form=form)

@movies_bp.route('/<int:movie_id>')
def detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    people = Person.query.all()
    rated_ids = {r.person_id for r in movie.ratings}
    return render_template('movies/detail.html', movie=movie, people=people, rated_ids=rated_ids)