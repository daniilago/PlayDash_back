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
    links = [
        {"name": "Ver Banco de Bagos", "url": url_for("display_db.display_db")},
        {"name": "Inserir dados", "url": url_for("insert.insert")},
        {"name": "Deletar dados", "url": url_for("delete.delete")},
        {"name": "Consultar dados", "url": url_for("querie.querie")},
    ]

    return render_template("home.html", links=links)
