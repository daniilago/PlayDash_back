from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from playdash.db import get_db

bp = Blueprint('delete', __name__, url_prefix='/delete')

@bp.route('/', methods=('GET',))
def delete():
    links = [
        {"name": "Delete Team", "url": url_for('delete.delete_teams')},
        {"name": "Delete Player", "url": url_for('delete.delete_players')},
        {"name": "Delete Coach", "url": url_for('delete.delete_coaches')},
        {"name": "Delete Match", "url": url_for('delete.delete_matches')},
        {"name": "Delete Event", "url": url_for('delete.delete_events')},
    ]
    return render_template('delete/delete.html', links=links)

@bp.route('/teams', methods=('GET', 'POST'))
def delete_teams():
    db = get_db()
    if request.method == 'POST':
        team_name = request.form['team_name']
        db.execute('DELETE FROM "time" WHERE nome_time = ?', (team_name,))
        db.commit()
        flash(f'Team {team_name} deleted.')
        return render_template('delete/delete_teams.html', teams=teams)

    teams = db.execute('SELECT * FROM "time"').fetchall()
    return render_template('delete/delete_teams.html', teams=teams)

@bp.route('/players', methods=('GET', 'POST'))
def delete_players():
    db = get_db()
    if request.method == 'POST':
        number = request.form['number']
        team_name = request.form['team_name']
        db.execute('DELETE FROM jogador WHERE numero = ? AND nome_time = ?', (number, team_name))
        db.commit()
        flash('Player deleted.')
        return redirect(url_for('delete.delete_players'))

    players = db.execute('SELECT * FROM jogador').fetchall()
    return render_template('delete/delete_players.html', players=players)

@bp.route('/coaches', methods=('GET', 'POST'))
def delete_coaches():
    db = get_db()
    if request.method == 'POST':
        coach_name = request.form['coach_name']
        db.execute('DELETE FROM tecnico WHERE nome_tecnico = ?', (coach_name,))
        db.commit()
        flash('Coach deleted.')
        return redirect(url_for('delete.delete_coaches'))

    coaches = db.execute('SELECT * FROM tecnico').fetchall()
    return render_template('delete/delete_coaches.html', coaches=coaches)

@bp.route('/matches', methods=('GET', 'POST'))
def delete_matches():
    db = get_db()
    if request.method == 'POST':
        match_id = request.form['match_id']
        db.execute('DELETE FROM partida WHERE id_partida = ?', (match_id,))
        db.commit()
        flash('Match deleted.')
        return redirect(url_for('delete.delete_matches'))

    matches = db.execute('SELECT * FROM partida').fetchall()
    return render_template('delete/delete_matches.html', matches=matches)

@bp.route('/events', methods=('GET', 'POST'))
def delete_events():
    db = get_db()
    if request.method == 'POST':
        event_id = request.form['event_id']
        db.execute('DELETE FROM evento WHERE id_evento = ?', (event_id,))
        db.commit()
        flash('Event deleted.')
        return redirect(url_for('delete.delete_events'))

    events = db.execute('SELECT * FROM evento').fetchall()
    return render_template('delete/delete_events.html', events=events)

@bp.route('/users', methods=('GET', 'POST'))
def delete_users():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        db.execute('DELETE FROM usuario WHERE username = ?', (username,))
        db.commit()
        flash('User deleted.')
        return redirect(url_for('delete.delete_users'))

    users = db.execute('SELECT * FROM usuario').fetchall()
    return render_template('delete/delete_users.html', users=users)
