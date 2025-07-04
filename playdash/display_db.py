from flask import Blueprint, render_template, url_for, redirect, g, flash

from playdash.db import get_db
from playdash.schema import User

bp = Blueprint("display_db", __name__, url_prefix="/display_db")


@bp.before_request
def require_login():
    if g.user is None:
        flash("Faça login para acessar esta página.")
        return redirect(url_for("auth.login"))


@bp.route("/users", methods=("GET", "POST"))
def display_users():
    db = get_db()
    users = db.execute("SELECT name, email, user_type FROM user").fetchall()
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
