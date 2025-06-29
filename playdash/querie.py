from flask import Blueprint, render_template, request, redirect, url_for, flash
from playdash.db import get_db

bp = Blueprint("querie", __name__, url_prefix="/querie")


@bp.route("/", methods=("GET",))
def querie():
    links = [
        {"name": "Consultar Time", "url": url_for("querie.querie_teams")},
        {"name": "Consultar Jogador", "url": url_for("querie.querie_players")},
        {"name": "Consultar Técnico", "url": url_for("querie.querie_coaches")},
        {"name": "Consultar Partida", "url": url_for("querie.querie_matches")},
        {"name": "Consultar Evento", "url": url_for("querie.querie_events")},
    ]
    return render_template("querie/querie.html", links=links)


@bp.route("/teams", methods=("GET", "POST"))
def querie_teams():
    db = get_db()
    if request.method == "POST":
        team_name = request.form["team_name"]
        teams = db.execute(
            'SELECT * FROM "time" WHERE nome_time LIKE ?', (f"%{team_name}%",)
        ).fetchall()
    else:
        teams = db.execute('SELECT * FROM "time"').fetchall()
    return render_template("querie/querie_teams.html", teams=teams)


@bp.route("/players", methods=("GET", "POST"))
def querie_players():
    db = get_db()
    if request.method == "POST":
        number = request.form["number"]
        team_name = request.form["team_name"]
        player_name = request.form["player_name"]

        query = "SELECT * FROM jogador WHERE 1=1"
        params = []
        if number:
            query += " AND numero = ?"
            params.append(number)
        if team_name:
            query += " AND nome_time LIKE ?"
            params.append(f"%{team_name}%")
        if player_name:
            query += " AND nome_jogador LIKE ?"
            params.append(f"%{player_name}%")

        players = db.execute(query, tuple(params)).fetchall()
    else:
        players = db.execute("SELECT * FROM jogador").fetchall()
    return render_template("querie/querie_players.html", players=players)


@bp.route("/coaches", methods=("GET", "POST"))
def querie_coaches():
    db = get_db()
    if request.method == "POST":
        team_name = request.form["team_name"]
        coach_name = request.form["coach_name"]

        query = "SELECT * FROM tecnico WHERE 1=1"
        params = []
        if team_name:
            query += " AND nome_time LIKE ?"
            params.append(f"%{team_name}%")
        if coach_name:
            query += " AND nome_tecnico LIKE ?"
            params.append(f"%{coach_name}%")

        coaches = db.execute(query, tuple(params)).fetchall()
    else:
        coaches = db.execute("SELECT * FROM tecnico").fetchall()
    return render_template("querie/querie_coaches.html", coaches=coaches)


@bp.route("/matches", methods=("GET", "POST"))
def querie_matches():
    db = get_db()
    if request.method == "POST":
        location = request.form.get("location")
        team1 = request.form.get("team1")
        team2 = request.form.get("team2")

        query = "SELECT * FROM partida WHERE 1=1"
        params = []

        if location:
            query += " AND local_partida LIKE ?"
            params.append(f"%{location}%")

        if team1 and team2:
            query += " AND ((time_casa_nome LIKE ? AND time_visitante_nome LIKE ?) OR (time_casa_nome LIKE ? AND time_visitante_nome LIKE ?))"
            params.extend([f"%{team1}%", f"%{team2}%", f"%{team2}%", f"%{team1}%"])
        elif team1:
            query += " AND (time_casa_nome LIKE ? OR time_visitante_nome LIKE ?)"
            params.extend([f"%{team1}%", f"%{team1}%"])

        matches = db.execute(query, tuple(params)).fetchall()
    else:
        matches = db.execute("SELECT * FROM partida").fetchall()
    return render_template("querie/querie_matches.html", matches=matches)


@bp.route("/events", methods=("GET", "POST"))
def querie_events():
    db = get_db()
    query = """
        SELECT e.id_evento, e.id_partida, e.tipo_do_evento, e.data_horario,
               e.jogador_time, j.nome_jogador
        FROM evento e
        JOIN jogador j ON e.jogador_numero = j.numero AND e.jogador_time = j.nome_time
        WHERE 1=1
    """
    params = []

    if request.method == "POST":
        event_type = request.form.get("event_type")
        player_name = request.form.get("player_name")
        match_id = request.form.get("match_id")

        if event_type:
            query += " AND e.tipo_do_evento LIKE ?"
            params.append(f"%{event_type}%")
        if player_name:
            query += " AND j.nome_jogador LIKE ?"
            params.append(f"%{player_name}%")
        if match_id:
            query += " AND e.id_partida = ?"
            params.append(match_id)

    events = db.execute(query, params).fetchall()
    return render_template("querie/querie_events.html", events=events)
