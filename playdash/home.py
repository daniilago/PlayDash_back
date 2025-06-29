from flask import Blueprint, render_template, url_for, redirect

bp = Blueprint(
    "home",
    __name__,
)


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
