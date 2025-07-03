from flask import Blueprint, render_template, url_for, redirect, g, flash

from playdash.db import get_db

bp = Blueprint("display_db", __name__, url_prefix="/display_db")


@bp.before_request
def require_login():
    if g.user is None:
        flash("Faça login para acessar esta página.")
        return redirect(url_for("auth.login"))

@bp.route("/", methods=("GET", "POST"))
def display_db():
    links = [
        {"name": "Ver Usuários", "url": url_for("display_db.display_users")},
        {"name": "Ver Times", "url": url_for("display_db.display_teams")},
        {"name": "Ver Jogadores", "url": url_for("display_db.display_players")},
        {"name": "Ver Técnicos", "url": url_for("display_db.display_coaches")},
        {"name": "Ver Partidas", "url": url_for("display_db.display_matches")},
        {"name": "Ver Eventos", "url": url_for("display_db.display_events")},
    ]

    return render_template("display_db/display_db.html", links=links)


@bp.route("/users", methods=("GET", "POST"))
def display_users():
    db = get_db()
    users = db.execute("SELECT * FROM user").fetchall()

    return render_template("display_db/display_users.html", users=users)


@bp.route("/teams", methods=("GET", "POST"))
def display_teams():
    db = get_db()
    teams = db.execute("SELECT * FROM team").fetchall()

    return render_template("display_db/display_teams.html", teams=teams)


@bp.route("/players", methods=("GET", "POST"))
def display_players():
    db = get_db()
    players = db.execute("SELECT * FROM player").fetchall()

    return render_template("display_db/display_players.html", players=players)


@bp.route("/coaches", methods=("GET", "POST"))
def display_coaches():
    db = get_db()
    coaches = db.execute("SELECT * FROM coach").fetchall()

    return render_template("display_db/display_coaches.html", coaches=coaches)


@bp.route("/matches", methods=("GET", "POST"))
def display_matches():
    db = get_db()
    matches = db.execute("SELECT * FROM match").fetchall()

    return render_template("display_db/display_matches.html", matches=matches)


@bp.route("/events", methods=("GET", "POST"))
def display_events():
    db = get_db()
    events = db.execute("SELECT * FROM event").fetchall()

    return render_template("display_db/display_events.html", events=events)
