from app import db
from datetime import datetime

class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ratings = db.relationship('Rating', backref='person', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Person {self.name}>'


class Movie(db.Model):
    __tablename__ = 'movies'   # add this so FK matches
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(10))
    genre = db.Column(db.String(255))
    imdb_link = db.Column(db.String(500))
    imdb_id = db.Column(db.String(20))

    ratings = db.relationship('Rating', backref='movie', lazy=True, cascade='all, delete-orphan')

    def average_score(self):
        if not self.ratings:
            return None
        return round(sum(r.score for r in self.ratings) / len(self.ratings), 2)

    def __repr__(self):
        return f'<Movie {self.title} ({self.year})>'


class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)  # 1-4
    notes = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('person_id', 'movie_id', name='unique_person_movie'),
    )

    def __repr__(self):
        return f'<Rating {self.person_id} -> {self.movie_id}: {self.score}>'