import os
from flask import Flask, send_from_directory
from flask_openapi3 import OpenAPI

UPLOAD_FOLDER = "images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def create_app(test_config=None):
    # create and configure the app
    app = OpenAPI(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flask.sqlite"),
    )
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    from . import home, auth, display_db, insert, delete, querie, api

    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(display_db.bp)
    app.register_blueprint(insert.bp)
    app.register_blueprint(delete.bp)
    app.register_blueprint(querie.bp)
    app.register_api(api.bp)

    @app.route("/public/<path:path>")
    def public_files(path):
        from pathlib import Path

        assert path is not None
        return send_from_directory(Path(UPLOAD_FOLDER).absolute(), path)

    del public_files

    return app
