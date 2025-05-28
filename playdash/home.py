from flask import(
    Blueprint, render_template, url_for
)

bp = Blueprint('home', __name__,)

@bp.route('/', methods=('GET', 'POST'))
def home():
    link = {"name": "Ver Banco de Bagos", "url": url_for('display_db.display_db')}

    return render_template('home.html', link=link)