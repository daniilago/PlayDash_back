from flask import Blueprint, render_template, url_for, request, redirect, flash

from playdash.db import get_db
from playdash import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from flask import current_app
import os

bp = Blueprint("insert", __name__, url_prefix="/insert")
EMBLEM_FOLDER = "emblems"
PLAYER_PHOTO_FOLDER = "player_photos"
COACH_PHOTO_FOLDER = "coach_photos"


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
                'SELECT 1 FROM "time" WHERE nome_time = ?', (team_name,)
            ).fetchone()
            if existing_team:
                error = f"Time '{team_name}' já existe"
            else:
                filename = (
                    team_name.replace(" ", "_") + os.path.splitext(emblem.filename)[1]
                )
                emblem.save(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"], EMBLEM_FOLDER, filename
                    )
                )
                db.execute(
                    'INSERT INTO "time" (nome_time, brasao) VALUES (?, ?)',
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
        number = request.form["number"]
        team_name = request.form["team_name"]
        photo = request.files["photo"]

        error = None

        if (
            not player_name
            or not birth_date
            or not nationality
            or not position
            or not number
            or not team_name
        ):
            error = "Todos os campos são obrigatórios."
        elif "photo" not in request.files or photo.filename == "":
            error = "Foto é obrigatória."
        elif photo and not allowed_file(photo.filename):
            error = "Formato de imagem inválido."

        if error is None:
            player_name = secure_filename(player_name)
            player_name = player_name.replace("_", " ")
            filename = (
                team_name.replace(" ", "_")
                + "_"
                + secure_filename(number)
                + os.path.splitext(photo.filename)[1]
            )

            try:
                db.execute(
                    """
                    INSERT INTO jogador (
                        nome_jogador, data_nascimento, nacionalidade,
                        foto, posicao, numero, nome_time
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        player_name,
                        birth_date,
                        nationality,
                        filename,
                        position,
                        number,
                        team_name,
                    ),
                )
                db.commit()
                photo.save(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"],
                        PLAYER_PHOTO_FOLDER,
                        filename,
                    )
                )
                return redirect(url_for("insert.insert_players"))
            except db.IntegrityError:
                error = f"Jogador com número {number} já existe no time {team_name}."

        flash(error)

    teams = db.execute('SELECT nome_time FROM "time"').fetchall()
    players = db.execute("SELECT * FROM jogador").fetchall()

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
            coach_name = secure_filename(coach_name)
            coach_name = coach_name.replace("_", " ")
            filename = (
                secure_filename(team_name.replace(" ", "_"))
                + "_coach"
                + os.path.splitext(photo.filename)[1]
            )
            try:
                db.execute(
                    """
                    INSERT INTO tecnico (
                        nome_tecnico, data_nascimento, nacionalidade,
                        foto, nome_time
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (coach_name, birth_date, nationality, filename, team_name),
                )
                db.commit()
                photo.save(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"],
                        COACH_PHOTO_FOLDER,
                        filename,
                    )
                )
                return redirect(url_for("insert.insert_coaches"))
            except db.IntegrityError:
                error = f"Já existe um técnico no time {team_name}."

        flash(error)
    teams = db.execute('SELECT nome_time FROM "time"').fetchall()
    coaches = db.execute("SELECT * FROM tecnico").fetchall()

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
                    INSERT INTO partida (
                        data_horario, local_partida,
                        time_casa_nome, time_visitante_nome
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (match_datetime, match_location, home_team, away_team),
                )
                db.commit()
                return redirect(url_for("insert.insert_matches"))
            except db.IntegrityError as e:
                error = "An error occurred while inserting the match."

        flash(error)

    teams = db.execute('SELECT nome_time FROM "time"').fetchall()
    matches = db.execute("SELECT * FROM partida").fetchall()

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
            error = "Player number is required."
        elif not player_team:
            error = "Player team is required."
        elif not event_type:
            error = "Event type is required."

        if error is None:
            # Mapear tipos de evento para prefixos
            event_prefix_map = {
                "gol": 1,
                "falta": 2,
                "cartao_amarelo": 3,
                "cartao_vermelho": 4,
            }

            # Obter o prefixo do tipo de evento
            event_prefix = event_prefix_map.get(event_type)
            if event_prefix is None:
                error = "Invalid event type."
            else:
                # Calcular o próximo ID do evento
                prefix = f"{event_prefix}0000"  # Exemplo: 10000 para gols
                last_event = db.execute(
                    """
                    SELECT id_evento FROM evento
                    WHERE id_evento >= ? AND id_evento < ?
                    ORDER BY id_evento DESC LIMIT 1
                    """,
                    (int(prefix), int(prefix) + 10000),
                ).fetchone()

                if last_event:
                    next_id = last_event["id_evento"] + 1
                else:
                    next_id = int(prefix)  # Primeiro ID para este tipo de evento

            try:
                # Inserir o evento no banco de dados
                db.execute(
                    """
                    INSERT INTO evento (id_evento, id_partida, data_horario, jogador_numero, jogador_time, tipo_do_evento)
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

    matches = db.execute("SELECT id_partida FROM partida").fetchall()
    players = db.execute(
        "SELECT numero AS jogador_numero, nome_time FROM jogador"
    ).fetchall()
    event_types = ["gol", "falta", "cartao_amarelo", "cartao_vermelho"]

    return render_template(
        "insert/insert_events.html",
        matches=matches,
        players=players,
        event_types=event_types,
    )
