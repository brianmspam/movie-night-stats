from flask import Blueprint, request, redirect, url_for, flash
from app.models import Rating, Movie, Person
from app import db

ratings_bp = Blueprint('ratings', __name__)

@ratings_bp.route('/add', methods=['POST'])
def add_rating():
    movie_id = request.form.get('movie_id')
    person_id = request.form.get('person_id')
    score = request.form.get('score')
    notes = request.form.get('notes', '').strip() or None

    if not all([movie_id, person_id, score]):
        flash('Movie, person, and score are all required.', 'error')
        return redirect(url_for('movies.list_movies'))

    score = int(score)
    if score < 1 or score > 4:
        flash('Score must be between 1 and 4.', 'error')
        return redirect(url_for('movies.detail', movie_id=movie_id))

    existing = Rating.query.filter_by(person_id=person_id, movie_id=movie_id).first()
    if existing:
        existing.score = score
        existing.notes = notes
        flash('Rating updated!', 'success')
    else:
        rating = Rating(score=score, notes=notes, person_id=person_id, movie_id=movie_id)
        db.session.add(rating)
        flash('Rating saved!', 'success')

    db.session.commit()
    return redirect(url_for('movies.detail', movie_id=movie_id))