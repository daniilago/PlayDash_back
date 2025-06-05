from flask import(
    Blueprint, render_template, url_for, request, redirect, flash
)

from playdash.db import get_db

bp = Blueprint('insert', __name__, url_prefix='/insert')

@bp.route('/', methods=('GET', 'POST'))
def insert():
    links =[
        {"name": "Inserir Time", "url": url_for('insert.insert_teams')},
        {"name": "Inserir Jogador", "url": url_for('insert.insert_players')},
        {"name": "Inserir Treinador", "url": url_for('insert.insert_coaches')},
        {"name": "Inserir Partida", "url": url_for('insert.insert_matches')},
        {"name": "Inserir Evento", "url": url_for('insert.insert_events')},
    ]

    return render_template('insert/insert.html', links=links)

@bp.route('/teams', methods=('GET', 'POST'))
def insert_teams():
    if request.method == 'POST':
        team_name = request.form['team_name']
        emblem = request.form['emblem']

        db = get_db()
        error = None

        if not team_name:
            error = 'Nome do time é necessário'
        elif not emblem:
            error = 'Brasão é necessário'

        if error is None:
            existing_team = db.execute(
                'SELECT 1 FROM "time" WHERE nome_time = ?', (team_name,)
            ).fetchone()
            if existing_team is None:
                db.execute(
                    'INSERT INTO "time" (nome_time, brasao) VALUES (?, ?)',
                    (team_name, emblem)
                )
                db.commit()
            else:
                error = f"Time '{team_name}' já existe"
                flash(error)
            
        if error is not None:
            flash(error)

    return render_template('insert/insert_teams.html')

@bp.route('/players', methods=('GET', 'POST'))
def insert_players():
    db = get_db()
    players = db.execute(
        'SELECT * FROM jogador'
    ).fetchall()

    return render_template('insert/insert_players.html', players=players)

@bp.route('/coaches', methods=('GET', 'POST'))
def insert_coaches():
    db = get_db()
    coaches = db.execute(
        'SELECT * FROM tecnico'
    ).fetchall()

    return render_template('insert/insert_coaches.html', coaches=coaches)

@bp.route('/matches', methods=('GET', 'POST'))
def insert_matches():
    db = get_db()
    matches = db.execute(
        'SELECT * FROM partida'
    ).fetchall()

    return render_template('insert/insert_matches.html', matches=matches)

@bp.route('/events', methods=('GET', 'POST'))
def insert_events():
    db = get_db()
    matches = db.execute('SELECT id_partida FROM partida').fetchall()
    players = db.execute('SELECT numero, nome_time FROM jogador').fetchall()
    event_types = ['Gol', 'Falta', 'Cartão Amarelo', 'Cartão Vermelho']

    if request.method == 'POST':
        event_id = request.form['event_id']
        match_id = request.form['match_id']
        date_hour = request.form['date_hour']
        player_number = request.form['player_number']
        player_team = request.form['player_team']
        event_type = request.form['event_type']

        error = None

        if not event_id:
            error = ''
        elif not match_id:
            error = ''
        elif not date_hour:
            error = ''
        elif not player_number:
            error = ''
        elif not player_team:
            error = ''
        elif not event_type:
            error = ''

        if error is None:
            existing_team = db.execute(
                'SELECT 1 FROM evento WHERE id_evento = ? AND id_partida = ?', (event_id, match_id,)
            ).fetchone()
            if existing_team is None:
                db.execute(
                    'INSERT INTO evento (id_evento, id_partida, data_horario, jogador_numero, jogador_time, tipo_do_evento) VALUES (?, ?, ?, ?, ?, ?)',
                    (event_id, match_id, date_hour, player_number, player_team, event_type)
                )
                db.commit()
            else:
                error = f"Evento já existe"
                flash(error)
            
        if error is not None:
            flash(error)

    return render_template('insert/insert_events.html', matches=matches, players=players, event_types=event_types)