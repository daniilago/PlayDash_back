from flask import Blueprint, flash, g, render_template, request
from playdash.db import get_db

bp = Blueprint('rotas', __name__)

@bp.route("/penis", methods=('GET',))
def pessoas():
    db = get_db()
    resultado = []
    for pessoa in db.execute("select id, name from pessoa;").fetchall():
        resultado.append(tuple(pessoa))
    return render_template('base.html', corpo=str(resultado))

@bp.route("/create_penis", methods=('GET',))
def pessoas_post():
    nome = request.args.get('nome')
    print(f"nome: {nome}")
    return render_template('base.html', corpo=str(nome))