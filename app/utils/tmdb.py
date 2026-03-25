# app/utils/tmdb.py
import os
import requests
from urllib.parse import urlparse

TMDB_API_KEY = os.environ.get("56f62ffdfb05bf4f97a3c1bfa25611a1")

class TMDBError(Exception):
    pass

class TMDBError(Exception):
    pass

def tmdb_movie_details(tmdb_id: int) -> dict:
    if not TMDB_API_KEY:
        raise TMDBError("TMDB_API_KEY not configured")

    r = requests.get(
        f"https://api.themoviedb.org/3/movie/{tmdb_id}",
        params={"api_key": TMDB_API_KEY, "language": "en-US"},
        timeout=10,
    )
    data = r.json()
    if r.status_code != 200 or "title" not in data:
        raise TMDBError("Error fetching movie details")
    return data

def fetch_movie_from_tmdb_url(tmdb_url: str) -> dict:
    tmdb_id = tmdb_url_to_tmdb_id(tmdb_url)
    if not tmdb_id:
        raise TMDBError("Not a valid TMDb movie URL")

    details = tmdb_movie_details(tmdb_id)

    return {
        "tmdb_id": tmdb_id,
        "tmdb_link": tmdb_url,
        "title": details.get("title"),
        "year": (details.get("release_date") or "")[:4],
        "genre": ", ".join(g["name"] for g in details.get("genres", [])),
    }