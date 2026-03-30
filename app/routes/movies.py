import os 
import requests

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db
from app.models import Movie, Rating, Person
from app.utils.tmdb import fetch_movie_from_tmdb_url, tmdb_url_to_tmdb_id, TMDBError

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
    if request.method == "POST" and "fetch_tmdb" in request.form and request.form.get("tmdb_url"):
        url = request.form["tmdb_url"]
        try:
            data = fetch_movie_from_tmdb_url(url)
            return render_template(
                "movies/add.html",
                tmdb_url=url,
                title=data["title"],
                year=data["year"],
                genre=data["genre"],
            )
        except TMDBError as e:
            flash(f"Could not load from TMDb: {e}", "danger")
            return render_template("movies/add.html", tmdb_url=url)

    if request.method == "POST" and "save" in request.form:
        tmdb_url = request.form.get("tmdb_url") or None
        data = {}
        if tmdb_url:
            try:
                data = fetch_movie_from_tmdb_url(tmdb_url)
            except TMDBError:
                data = {}

        movie = Movie(
            title=request.form.get("title") or data.get("title"),
            year=request.form.get("year") or data.get("year"),
            genre=request.form.get("genre") or data.get("genre"),
            tmdb_id=data.get("tmdb_id"),
            tmdb_link=tmdb_url,
        )
        db.session.add(movie)
        db.session.commit()
        flash("Movie added.", "success")
        return redirect(url_for("main.index"))

        # GET: pre-fill from TMDb
    title = request.args.get("title", "")
    year = request.args.get("year", "")
    tmdb_id = request.args.get("tmdb_id", "")

    return render_template("movies/add.html")

@movies_bp.route("/<int:movie_id>")
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    people = Person.query.order_by(Person.name).all()
    return render_template("movies/detail.html", movie=movie, people=people)