from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Person
from app import db

people_bp = Blueprint('people', __name__)

@people_bp.route('/')
def list_people():
    people = Person.query.order_by(Person.name).all()
    return render_template('people/list.html', people=people)

@people_bp.route('/add', methods=['POST'])
def add_person():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Name is required.', 'error')
        return redirect(url_for('people.list_people'))
    if Person.query.filter_by(name=name).first():
        flash(f'"{name}" already exists.', 'error')
        return redirect(url_for('people.list_people'))
    person = Person(name=name)
    db.session.add(person)
    db.session.commit()
    flash(f'"{name}" added!', 'success')
    return redirect(url_for('people.list_people'))