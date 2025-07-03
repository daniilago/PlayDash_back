from flask import Blueprint, render_template, request, redirect, url_for, flash
from playdash.db import get_db

bp = Blueprint("delete", __name__, url_prefix="/delete")


@bp.route("/", methods=("GET",))
def delete():
    links = [
        {"name": "Deletar Time", "url": url_for("delete.delete_teams")},
        {"name": "Deletar Jogador", "url": url_for("delete.delete_players")},
        {"name": "Deletar Técnico", "url": url_for("delete.delete_coaches")},
        {"name": "Deletar Partida", "url": url_for("delete.delete_matches")},
        {"name": "Deletar Evento", "url": url_for("delete.delete_events")},
    ]
    return render_template("delete/delete.html", links=links)


@bp.route("/teams", methods=("GET", "POST"))
def delete_teams():
    db = get_db()
    if request.method == "POST":
        team_name = request.form["team_name"]
        db.execute('DELETE FROM team WHERE name = ?', (team_name,))
        db.commit()
        flash(f"Time {team_name} deletado.")
        return redirect(url_for("delete.delete_teams"))

    teams = db.execute('SELECT * FROM team').fetchall()
    return render_template("delete/delete_teams.html", teams=teams)


@bp.route("/players", methods=("GET", "POST"))
def delete_players():
    db = get_db()
    if request.method == "POST":
        shirt_number = request.form["shirt_number"]
        team_name = request.form["team_name"]
        db.execute(
            "DELETE FROM player WHERE shirt_number = ? AND team_name = ?",
            (shirt_number, team_name),
        )
        db.commit()
        flash("Jogador deletado.")
        return redirect(url_for("delete.delete_players"))

    players = db.execute("SELECT * FROM player").fetchall()
    return render_template("delete/delete_players.html", players=players)


@bp.route("/coaches", methods=("GET", "POST"))
def delete_coaches():
    db = get_db()
    if request.method == "POST":
        coach_name = request.form["coach_name"]
        db.execute("DELETE FROM coach WHERE name = ?", (coach_name,))
        db.commit()
        flash("Técnico deletado.")
        return redirect(url_for("delete.delete_coaches"))

    coaches = db.execute("SELECT * FROM coach").fetchall()
    return render_template("delete/delete_coaches.html", coaches=coaches)


@bp.route("/matches", methods=("GET", "POST"))
def delete_matches():
    db = get_db()
    if request.method == "POST":
        match_id = request.form["match_id"]
        db.execute("DELETE FROM match WHERE id = ?", (match_id,))
        db.commit()
        flash("Partida deletada.")
        return redirect(url_for("delete.delete_matches"))

    matches = db.execute("SELECT * FROM match").fetchall()
    return render_template("delete/delete_matches.html", matches=matches)


@bp.route("/events", methods=("GET", "POST"))
def delete_events():
    db = get_db()
    if request.method == "POST":
        event_id = request.form["event_id"]
        db.execute("DELETE FROM event WHERE id = ?", (event_id,))
        db.commit()
        flash("Evento deletado.")
        return redirect(url_for("delete.delete_events"))

    events = db.execute("SELECT * FROM event").fetchall()
    return render_template("delete/delete_events.html", events=events)
