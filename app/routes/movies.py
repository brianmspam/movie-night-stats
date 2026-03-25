from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Movie
from app.utils.tmdb import fetch_movie_from_imdb_url_tmdb, imdb_url_to_imdb_id, TMDBError

movies_bp = Blueprint("movies", __name__)

@movies_bp.route('/')
def list_movies():
    query = request.args.get('q', '')
    if query:
        movies = Movie.query.filter(Movie.title.ilike(f'%{query}%')).order_by(Movie.added.desc()).all()
    else:
        movies = Movie.query.order_by(Movie.added.desc()).all()
    return render_template('movies/list.html', movies=movies, query=query)

@movies_bp.route("/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST" and "fetch_imdb" in request.form and request.form.get("imdb_url"):
        try:
            data = fetch_movie_from_imdb_url_tmdb(request.form["imdb_url"])
            return render_template(
                "movies/add.html",
                imdb_url=request.form["imdb_url"],
                title=data["title"],
                year=data["year"],
                genre=data["genre"],
            )
        except TMDBError as e:
            flash(f"Could not load from TMDb: {e}", "danger")
            return render_template("movies/add.html", imdb_url=request.form.get("imdb_url"))

    if request.method == "POST" and "save" in request.form:
        movie = Movie(
            title=request.form.get("title"),
            year=request.form.get("year"),
            genre=request.form.get("genre"),
            imdb_link=request.form.get("imdb_url") or None,
            imdb_id=imdb_url_to_imdb_id(request.form.get("imdb_url")) if request.form.get("imdb_url") else None,
        )
        db.session.add(movie)
        db.session.commit()
        flash("Movie added.", "success")
        return redirect(url_for("main.index"))

    return render_template("movies/add.html")

@movies_bp.route('/<int:movie_id>')
def detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    people = Person.query.all()
    rated_ids = {r.person_id for r in movie.ratings}
    return render_template('movies/detail.html', movie=movie, people=people, rated_ids=rated_ids)