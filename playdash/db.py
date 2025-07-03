import sqlite3
from datetime import datetime
import click
from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command("drop-db")
def drop_db_command():
    """Drop all tables from the database."""
    db = get_db()
    # Adapte os nomes das tabelas conforme seu schema.sql
    db.executescript("""
        DROP TABLE IF EXISTS event;
        DROP TABLE IF EXISTS match;
        DROP TABLE IF EXISTS coach;
        DROP TABLE IF EXISTS player;
        DROP TABLE IF EXISTS team;
        DROP TABLE IF EXISTS user;
    """)
    db.commit()
    click.echo("Dropped all tables.")


@click.command("fill-db")
def fill_db_command():
    """Fill all tables from the database if they are empty."""
    db = get_db()

    # Usuário
    user_exists = db.execute("SELECT 1 FROM user LIMIT 1").fetchone()
    if not user_exists:
        db.execute(
            "INSERT INTO user (name, email, password, user_type) VALUES (?, ?, ?, ?)",
            ("admin", "admin@gmail.com", generate_password_hash("123"), "A"),
        )

    # Times
    team_exists = db.execute("SELECT 1 FROM team LIMIT 1").fetchone()
    if not team_exists:
        db.execute(
            "INSERT INTO team (name, emblem) VALUES (?, ?)",
            ("Flamengo", "a.jpg"),
        )
        db.execute(
            "INSERT INTO team (name, emblem) VALUES (?, ?)",
            ("Cruzeiro", "a.jpg"),
        )

    # Jogador
    player_exists = db.execute("SELECT 1 FROM player LIMIT 1").fetchone()
    if not player_exists:
        db.execute(
            """
            INSERT INTO player (
                name, date_of_birth, nationality,
                photo, position, shirt_number, team_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Pedro",
                "2025-07-08",
                "Brasileiro",
                "aa69.jpg",
                "atacante",
                23,
                "Flamengo",
            ),
        )

    # Técnico
    coach_exists = db.execute("SELECT 1 FROM coach LIMIT 1").fetchone()
    if not coach_exists:
        db.execute(
            """
            INSERT INTO coach (
                name, date_of_birth, nationality,
                photo, team_name
            ) VALUES (?, ?, ?, ?, ?)
            """,
            ("Tite", "2025-07-07", "Brasileiro", "a.jpg", "Flamengo"),
        )

    # Partida
    match_exists = db.execute("SELECT 1 FROM match LIMIT 1").fetchone()
    if not match_exists:
        db.execute(
            """
            INSERT INTO match (
                date_hour, location,
                home_team, visitor_team
            ) VALUES (?, ?, ?, ?)
            """,
            ("2025-07-26 02:06", "Rio de Janeiro", "Flamengo", "Cruzeiro"),
        )

    # Evento
    event_exists = db.execute("SELECT 1 FROM event LIMIT 1").fetchone()
    if not event_exists:
        db.execute(
            """
            INSERT INTO event (id, match_id, date_hour, player_number, player_team, event_type)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                10000,
                1,
                "2025-07-15 02:16",
                23,
                "Flamengo",
                "gol",
            ),
        )

    db.commit()
    click.echo("Filled all tables (if empty).")


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
    app.cli.add_command(fill_db_command)
