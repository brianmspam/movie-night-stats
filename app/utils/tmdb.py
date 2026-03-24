# app/utils/tmdb.py
import os
import requests
from urllib.parse import urlparse

TMDB_API_KEY = os.environ.get("56f62ffdfb05bf4f97a3c1bfa25611a1")

class TMDBError(Exception):
    pass

def imdb_url_to_imdb_id(url: str) -> str | None:
    path = urlparse(url).path  # "/title/tt0111161/"
    parts = [p for p in path.split("/") if p]
    return parts[1] if len(parts) >= 2 and parts[0] == "title" else None

def tmdb_find_by_imdb_id(imdb_id: str) -> dict:
    if not TMDB_API_KEY:
        raise TMDBError("TMDB_API_KEY not configured")

    r = requests.get(
        "https://api.themoviedb.org/3/find/" + imdb_id,
        params={"api_key": TMDB_API_KEY, "language": "en-US", "external_source": "imdb_id"},
        timeout=10,
    )
    data = r.json()
    results = data.get("movie_results") or []
    if not results:
        raise TMDBError(f"No TMDb movie found for {imdb_id}")
    return results[0]  # first match