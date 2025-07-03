from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from playdash.db import get_db

bp = Blueprint("querie", __name__, url_prefix="/querie")


@bp.before_request
def require_login():
    if g.user is None:
        flash("Faça login para acessar esta página.")
        return redirect(url_for("auth.login"))


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
            "SELECT * FROM team WHERE name LIKE ?", (f"%{team_name}%",)
        ).fetchall()
    else:
        teams = db.execute("SELECT * FROM team").fetchall()
    return render_template("querie/querie_teams.html", teams=teams)


@bp.route("/players", methods=("GET", "POST"))
def querie_players():
    db = get_db()
    if request.method == "POST":
        shirt_number = request.form["shirt_number"]
        team_name = request.form["team_name"]
        player_name = request.form["player_name"]

        query = "SELECT * FROM player WHERE 1=1"
        params = []
        if shirt_number:
            query += " AND shirt_number = ?"
            params.append(shirt_number)
        if team_name:
            query += " AND team_name LIKE ?"
            params.append(f"%{team_name}%")
        if player_name:
            query += " AND name LIKE ?"
            params.append(f"%{player_name}%")

        players = db.execute(query, tuple(params)).fetchall()
    else:
        players = db.execute("SELECT * FROM player").fetchall()
    return render_template("querie/querie_players.html", players=players)


@bp.route("/coaches", methods=("GET", "POST"))
def querie_coaches():
    db = get_db()
    if request.method == "POST":
        team_name = request.form["team_name"]
        coach_name = request.form["coach_name"]

        query = "SELECT * FROM coach WHERE 1=1"
        params = []
        if team_name:
            query += " AND team_name LIKE ?"
            params.append(f"%{team_name}%")
        if coach_name:
            query += " AND name LIKE ?"
            params.append(f"%{coach_name}%")

        coaches = db.execute(query, tuple(params)).fetchall()
    else:
        coaches = db.execute("SELECT * FROM coach").fetchall()
    return render_template("querie/querie_coaches.html", coaches=coaches)


@bp.route("/matches", methods=("GET", "POST"))
def querie_matches():
    db = get_db()
    if request.method == "POST":
        location = request.form.get("location")
        team1 = request.form.get("team1")
        team2 = request.form.get("team2")

        query = "SELECT * FROM match WHERE 1=1"
        params = []

        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")

        if team1 and team2:
            query += " AND ((home_team LIKE ? AND visitor_team LIKE ?) OR (home_team LIKE ? AND visitor_team LIKE ?))"
            params.extend([f"%{team1}%", f"%{team2}%", f"%{team2}%", f"%{team1}%"])
        elif team1:
            query += " AND (home_team LIKE ? OR visitor_team LIKE ?)"
            params.extend([f"%{team1}%", f"%{team1}%"])

        matches = db.execute(query, tuple(params)).fetchall()
    else:
        matches = db.execute("SELECT * FROM match").fetchall()
    return render_template("querie/querie_matches.html", matches=matches)


@bp.route("/events", methods=("GET", "POST"))
def querie_events():
    db = get_db()
    query = """
        SELECT e.id, e.match_id, e.event_type, e.date_hour,
               e.player_team, j.name
        FROM event e
        JOIN player j ON e.player_number = j.shirt_number AND e.player_team = j.name
        WHERE 1=1
    """
    params = []

    if request.method == "POST":
        event_type = request.form.get("event_type")
        player_name = request.form.get("player_name")
        match_id = request.form.get("match_id")

        if event_type:
            query += " AND e.event_type LIKE ?"
            params.append(f"%{event_type}%")
        if player_name:
            query += " AND j.name LIKE ?"
            params.append(f"%{player_name}%")
        if match_id:
            query += " AND e.match_id = ?"
            params.append(match_id)

    matches = db.execute("SELECT * from match").fetchall()

    events = db.execute(query, params).fetchall()
    return render_template("querie/querie_events.html", events=events, matches=matches)
