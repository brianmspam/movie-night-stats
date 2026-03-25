from flask import Blueprint, request, redirect, url_for, flash
from app.models import Rating, Movie, Person
from app import db

ratings_bp = Blueprint('ratings', __name__)

@ratings_bp.route('/add', methods=['POST'])
def add_rating():
    movie_id = request.form.get('movie_id')

    if not movie_id:
        flash('Movie is required.', 'error')
        return redirect(url_for('movies.list_movies'))

    movie = Movie.query.get_or_404(movie_id)
    people = Person.query.order_by(Person.name).all()

    any_updated = False

    for person in people:
        score_key = f'score_{person.id}'
        notes_key = f'notes_{person.id}'

        score_val = request.form.get(score_key)
        notes_val = (request.form.get(notes_key) or '').strip() or None

        # Did not watch: empty => exclude from ratings
        if not score_val:
            continue

        try:
            score = float(score_val)
        except ValueError:
            continue

        if score < 1.0 or score > 4.0:
            continue

        rating = Rating.query.filter_by(
            person_id=person.id, movie_id=movie.id
        ).first()
        if rating is None:
            rating = Rating(person_id=person.id, movie_id=movie.id)

        rating.score = score
        rating.notes = notes_val
        db.session.add(rating)
        any_updated = True

    if any_updated:
        db.session.commit()
        flash('Scores updated.', 'success')
    else:
        flash('No scores to update.', 'info')

    return redirect(url_for('movies.movie_detail', movie_id=movie_id))