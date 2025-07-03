from flask import Blueprint, render_template, url_for, redirect, flash, g


bp = Blueprint(
    "home",
    __name__,
)


@bp.before_request
def require_login():
    if g.user is None:
        flash("Faça login para acessar esta página.")
        return redirect(url_for("auth.login"))


@bp.route("/", methods=("GET", "POST"))
def index():
    return redirect(url_for("auth.login"))


@bp.route("/home", methods=("GET", "POST"))
def home():
    topics = [
        {"name": "Ver Banco de Dados"},
        {"name": "Inserir dados"},
        {"name": "Deletar dados"},
        {"name": "Consultar dados"},
    ]
    links1 = [
        {"name": "Ver Usuários", "url": url_for("display_db.display_users")},
        {"name": "Ver Times", "url": url_for("display_db.display_teams")},
        {"name": "Ver Jogadores", "url": url_for("display_db.display_players")},
        {"name": "Ver Técnicos", "url": url_for("display_db.display_coaches")},
        {"name": "Ver Partidas", "url": url_for("display_db.display_matches")},
        {"name": "Ver Eventos", "url": url_for("display_db.display_events")},
    ]
    links2 = [
        {"name": "Inserir Time", "url": url_for("insert.insert_teams")},
        {"name": "Inserir Jogador", "url": url_for("insert.insert_players")},
        {"name": "Inserir Técnico", "url": url_for("insert.insert_coaches")},
        {"name": "Inserir Partida", "url": url_for("insert.insert_matches")},
        {"name": "Inserir Evento", "url": url_for("insert.insert_events")},
    ]
    links3 = [
        {"name": "Deletar Time", "url": url_for("delete.delete_teams")},
        {"name": "Deletar Jogador", "url": url_for("delete.delete_players")},
        {"name": "Deletar Técnico", "url": url_for("delete.delete_coaches")},
        {"name": "Deletar Partida", "url": url_for("delete.delete_matches")},
        {"name": "Deletar Evento", "url": url_for("delete.delete_events")},
    ]
    links4 = [
        {"name": "Consultar Time", "url": url_for("querie.querie_teams")},
        {"name": "Consultar Jogador", "url": url_for("querie.querie_players")},
        {"name": "Consultar Técnico", "url": url_for("querie.querie_coaches")},
        {"name": "Consultar Partida", "url": url_for("querie.querie_matches")},
        {"name": "Consultar Evento", "url": url_for("querie.querie_events")},
    ]

    return render_template("home.html", topics=topics, links1=links1, links2=links2, links3=links3, links4=links4)
