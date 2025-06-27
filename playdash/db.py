import sqlite3
from datetime import datetime
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('drop-db')
def drop_db_command():
    """Drop all tables from the database."""
    db = get_db()
    # Adapte os nomes das tabelas conforme seu schema.sql
    db.executescript("""
        DROP TABLE IF EXISTS evento;
        DROP TABLE IF EXISTS partida;
        DROP TABLE IF EXISTS tecnico;
        DROP TABLE IF EXISTS jogador;
        DROP TABLE IF EXISTS "time";
        DROP TABLE IF EXISTS usuario;
    """)
    db.commit()
    click.echo('Dropped all tables.')
    

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)