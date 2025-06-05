from flask import(
    Blueprint, render_template, url_for
)

from playdash.db import get_db

bp = Blueprint('delete', __name__, url_prefix='/delete')

@bp.route('/', methods=('GET', 'POST'))
def delete():
    links =[
        {"name": "Deletar Time", "url": url_for('delete.delete_teams')},
        {"name": "Deletar Jogador", "url": url_for('delete.delete_players')},
        {"name": "Deletar Treinador", "url": url_for('delete.delete_coaches')},
        {"name": "Deletar Partida", "url": url_for('delete.delete_matches')},
        {"name": "Deletar Evento", "url": url_for('delete.delete_events')},
    ]

    return render_template('delete/delete.html', links=links)

@bp.route('/users', methods=('GET', 'POST'))
def delete_users():
    db = get_db()
    users = db.execute(
        'SELECT * FROM usuario'
    ).fetchall()

    return render_template('delete/delete_users.html', users=users)

@bp.route('/teams', methods=('GET', 'POST'))
def delete_teams():
    db = get_db()
    teams = db.execute(
        'SELECT * FROM time'
    ).fetchall()

    return render_template('delete/delete_teams.html', teams=teams)

@bp.route('/players', methods=('GET', 'POST'))
def delete_players():
    db = get_db()
    players = db.execute(
        'SELECT * FROM jogador'
    ).fetchall()

    return render_template('delete/delete_players.html', players=players)

@bp.route('/coaches', methods=('GET', 'POST'))
def delete_coaches():
    db = get_db()
    coaches = db.execute(
        'SELECT * FROM tecnico'
    ).fetchall()

    return render_template('delete/delete_coaches.html', coaches=coaches)

@bp.route('/matches', methods=('GET', 'POST'))
def delete_matches():
    db = get_db()
    matches = db.execute(
        'SELECT * FROM partida'
    ).fetchall()

    return render_template('delete/delete_matches.html', matches=matches)

@bp.route('/events', methods=('GET', 'POST'))
def delete_events():
    db = get_db()
    events = db.execute(
        'SELECT * FROM evento'
    ).fetchall()

    return render_template('delete/delete_events.html', events=events)