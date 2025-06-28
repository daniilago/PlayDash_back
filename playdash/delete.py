from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from playdash.db import get_db

bp = Blueprint('delete', __name__, url_prefix='/delete')

@bp.route('/', methods=('GET',))
def delete():
    links = [
        {"name": "Deletar Time", "url": url_for('delete.delete_teams')},
        {"name": "Deletar Jogador", "url": url_for('delete.delete_players')},
        {"name": "Deletar Técnico", "url": url_for('delete.delete_coaches')},
        {"name": "Deletar Partida", "url": url_for('delete.delete_matches')},
        {"name": "Deletar Evento", "url": url_for('delete.delete_events')},
    ]
    return render_template('delete/delete.html', links=links)

@bp.route('/teams', methods=('GET', 'POST'))
def delete_teams():
    db = get_db()
    if request.method == 'POST':
        team_name = request.form['team_name']
        db.execute('DELETE FROM "time" WHERE nome_time = ?', (team_name,))
        db.commit()
        flash(f'Time {team_name} deletado.')
        return redirect(url_for('delete.delete_teams'))

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
        flash('Jogador deletado.')
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
        flash('Técnico deletado.')
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
        flash('Partida deletada.')
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
        flash('Evento deletado.')
        return redirect(url_for('delete.delete_events'))

    events = db.execute('SELECT * FROM evento').fetchall()
    return render_template('delete/delete_events.html', events=events)
