from flask import Blueprint, render_template, url_for, request, redirect, flash

from playdash.db import get_db
from playdash import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from flask import current_app
from pathlib import Path
import os

bp = Blueprint("insert", __name__, url_prefix="/insert")


def save_file(name: str, file):
    filename = secure_filename(name) + os.path.splitext(file.filename)[1]
    file_path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
    os.makedirs(file_path.parent, exist_ok=True)

    file.save(file_path)
    return filename


@bp.route("/", methods=("GET", "POST"))
def insert():
    links = [
        {"name": "Inserir Time", "url": url_for("insert.insert_teams")},
        {"name": "Inserir Jogador", "url": url_for("insert.insert_players")},
        {"name": "Inserir Técnico", "url": url_for("insert.insert_coaches")},
        {"name": "Inserir Partida", "url": url_for("insert.insert_matches")},
        {"name": "Inserir Evento", "url": url_for("insert.insert_events")},
    ]

    return render_template("insert/insert.html", links=links)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/teams", methods=("GET", "POST"))
def insert_teams():
    if request.method == "POST":
        team_name = request.form["team_name"]
        emblem = request.files["emblem"]

        db = get_db()
        error = None

        if not team_name:
            error = "Nome do time é necessário"
        elif "emblem" not in request.files or emblem.filename == "":
            error = "Brasão é necessário"
        elif emblem and not allowed_file(emblem.filename):
            error = "Formato de arquivo inválido"

        if error is None:
            team_name = secure_filename(team_name)
            team_name.replace("_", " ")
            existing_team = db.execute(
                "SELECT 1 FROM team WHERE name = ?", (team_name,)
            ).fetchone()
            print(team_name, existing_team)
            if existing_team:
                error = f"Time '{team_name}' já existe"
            else:
                filename = save_file(team_name, emblem)
                db.execute(
                    "INSERT INTO team (name, emblem) VALUES (?, ?)",
                    (team_name, filename),
                )
                db.commit()
                return redirect(url_for("insert.insert_teams"))

        flash(error)
    return render_template("insert/insert_teams.html")


@bp.route("/players", methods=("GET", "POST"))
def insert_players():
    db = get_db()

    if request.method == "POST":
        player_name = request.form["player_name"]
        birth_date = request.form["birth_date"]
        nationality = request.form["nationality"]
        position = request.form["position"]
        shirt_number = request.form["shirt_number"]
        team_name = request.form["team_name"]
        photo = request.files["photo"]

        error = None

        if (
            not player_name
            or not birth_date
            or not nationality
            or not position
            or not shirt_number
            or not team_name
        ):
            error = "Todos os campos são obrigatórios."
        elif "photo" not in request.files or photo.filename == "":
            error = "Foto é obrigatória."
        elif photo and not allowed_file(photo.filename):
            error = "Formato de imagem inválido."

        if error is None:
            filename = save_file(team_name + player_name + str(shirt_number), photo)

            try:
                db.execute(
                    """
                    INSERT INTO player (
                        name, date_of_birth, nationality,
                        photo, position, shirt_number, team_name
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        player_name,
                        birth_date,
                        nationality,
                        filename,
                        position,
                        shirt_number,
                        team_name,
                    ),
                )
                db.commit()
                return redirect(url_for("insert.insert_players"))
            except db.IntegrityError:
                error = (
                    f"Jogador com número {shirt_number} já existe no time {team_name}."
                )

        flash(error)

    teams = db.execute("SELECT name FROM team").fetchall()
    players = db.execute("SELECT * FROM player").fetchall()

    return render_template("insert/insert_players.html", players=players, teams=teams)


@bp.route("/coaches", methods=("GET", "POST"))
def insert_coaches():
    db = get_db()

    if request.method == "POST":
        coach_name = request.form["coach_name"]
        birth_date = request.form["birth_date"]
        nationality = request.form["nationality"]
        team_name = request.form["team_name"]
        photo = request.files["photo"]

        error = None

        if (
            not coach_name
            or not birth_date
            or not nationality
            or not team_name
            or not photo
        ):
            error = "Todos os campos são obrigatórios."
        elif "photo" not in request.files or photo.filename == "":
            error = "Foto é obrigatória."
        elif photo and not allowed_file(photo.filename):
            error = "Formato de imagem inválido."

        if error is None:
            filename = save_file(coach_name, photo)
            try:
                db.execute(
                    """
                    INSERT INTO coach (
                        name, date_of_birth, nationality,
                        photo, team_name
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (coach_name, birth_date, nationality, filename, team_name),
                )
                db.commit()
                return redirect(url_for("insert.insert_coaches"))
            except db.IntegrityError:
                error = f"Já existe um técnico no time {team_name}."

        flash(error)
    teams = db.execute("SELECT name FROM team").fetchall()
    coaches = db.execute("SELECT * FROM coach").fetchall()

    return render_template("insert/insert_coaches.html", coaches=coaches, teams=teams)


@bp.route("/matches", methods=("GET", "POST"))
def insert_matches():
    db = get_db()
    error = None

    if request.method == "POST":
        match_datetime = request.form["match_datetime"]
        match_location = request.form["match_location"]
        home_team = request.form["home_team"]
        away_team = request.form["away_team"]

        if not match_datetime or not match_location or not home_team or not away_team:
            error = "All fields are required."
        elif home_team == away_team:
            error = "Home and away teams must be different."

        if error is None:
            try:
                db.execute(
                    """
                    INSERT INTO match (
                        date_hour, location,
                        home_team, visitor_team
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (match_datetime, match_location, home_team, away_team),
                )
                db.commit()
                return redirect(url_for("insert.insert_matches"))
            except db.IntegrityError as e:
                error = "An error occurred while inserting the match."

        flash(error)

    teams = db.execute("SELECT name FROM team").fetchall()
    matches = db.execute("SELECT * FROM match").fetchall()

    return render_template("insert/insert_matches.html", matches=matches, teams=teams)


@bp.route("/events", methods=("GET", "POST"))
def insert_events():
    db = get_db()
    error = None

    if request.method == "POST":
        match_id = request.form["match_id"]
        date_hour = request.form["date_hour"]
        player_number = request.form["player_number"]
        player_team = request.form["player_team"]
        event_type = request.form["event_type"]

        if not match_id:
            error = "Match ID is required."
        elif not date_hour:
            error = "Date and time are required."
        elif not player_number:
            error = "Player shirt_number is required."
        elif not player_team:
            error = "Player team is required."
        elif not event_type:
            error = "Event type is required."

        if error is None:
            # Mapear tipos de event para prefixos
            event_prefix_map = {
                "gol": 1,
                "falta": 2,
                "cartao_amarelo": 3,
                "cartao_vermelho": 4,
            }

            # Obter o prefixo do tipo de event
            event_prefix = event_prefix_map.get(event_type)
            if event_prefix is None:
                error = "Invalid event type."
            else:
                # Calcular o próximo ID do event
                prefix = f"{event_prefix}0000"  # Exemplo: 10000 para goals
                last_event = db.execute(
                    """
                    SELECT id FROM event
                    WHERE id >= ? AND id < ?
                    ORDER BY id DESC LIMIT 1
                    """,
                    (int(prefix), int(prefix) + 10000),
                ).fetchone()

                if last_event:
                    next_id = last_event["id"] + 1
                else:
                    next_id = int(prefix)  # Primeiro ID para este tipo de event

            try:
                # Inserir o event no banco de dados
                db.execute(
                    """
                    INSERT INTO event (id, match_id, date_hour, player_number, player_team, event_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        next_id,
                        match_id,
                        date_hour,
                        player_number,
                        player_team,
                        event_type,
                    ),
                )
                db.commit()
                return redirect(url_for("insert.insert_events"))
            except db.IntegrityError as e:
                error = "An error occurred while inserting the event."

        flash(error)

    matches = db.execute("SELECT id FROM match").fetchall()
    players = db.execute(
        "SELECT shirt_number AS player_number, name FROM player"
    ).fetchall()
    event_types = ["gol", "falta", "cartao_amarelo", "cartao_vermelho"]

    return render_template(
        "insert/insert_events.html",
        matches=matches,
        players=players,
        event_types=event_types,
    )
