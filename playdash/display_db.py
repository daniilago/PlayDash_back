from flask import(Blueprint, render_template)

from playdash.db import get_db

bp = Blueprint('display_db', __name__, url_prefix='/display_db')

@bp.route('/users', methods=('GET', 'POST'))
def display_users():
    db = get_db()
    users = db.execute(
        'SELECT * FROM usuario'
    ).fetchall()

    return render_template('display_db/display_users.html', users=users)

@bp.route('/teams', methods=('GET', 'POST'))
def display_teams():
    db = get_db()
    teams = db.execute(
        'SELECT * FROM time'
    ).fetchall()

    return render_template('display_db/display_teams.html', teams=teams)

@bp.route('/players', methods=('GET', 'POST'))
def display_players():
    db = get_db()
    players = db.execute(
        'SELECT * FROM jogador'
    ).fetchall()

    return render_template('display_db/display_players.html', players=players)

@bp.route('/coaches', methods=('GET', 'POST'))
def display_coaches():
    db = get_db()
    coaches = db.execute(
        'SELECT * FROM tecnico'
    ).fetchall()

    return render_template('display_db/display_coaches.html', coaches=coaches)

@bp.route('/matches', methods=('GET', 'POST'))
def display_matches():
    db = get_db()
    matches = db.execute(
        'SELECT * FROM partida'
    ).fetchall()

    return render_template('display_db/display_matches.html', matches=matches)

@bp.route('/events', methods=('GET', 'POST'))
def display_events():
    db = get_db()
    events = db.execute(
        'SELECT * FROM evento'
    ).fetchall()

    return render_template('display_db/display_events.html', events=events)