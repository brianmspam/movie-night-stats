# app/routes/tmdb.py
import os
import requests
from flask import Blueprint, render_template, request, current_app

tmdb_bp = Blueprint("tmdb", __name__, url_prefix="/tmdb")

@tmdb_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    results = []

    if query:
        api_key = current_app.config.get("TMDB_API_KEY") or os.getenv("TMDB_API_KEY")
        if api_key:
            r = requests.get(
                "https://api.themoviedb.org/3/search/movie",
                params={"api_key": api_key, "query": query},
                timeout=5,
            )
            data = r.json()
            results = data.get("results", [])

    return render_template("tmdb/search.html", query=query, results=results)