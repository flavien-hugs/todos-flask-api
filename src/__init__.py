import os
import logging

from flask import Flask, redirect

from src import exts
from src.config import settings


def create_todos_app(config_name):
    todos_app = Flask(__name__, instance_relative_config=True)
    todos_app.config.from_object(settings[config_name])
    settings[config_name].init_app(todos_app)

    todos_app.url_map.strict_slashes = False
    todos_app.jinja_env.globals.update(zip=zip)

    exts.db.init_app(todos_app)
    exts.ma.init_app(todos_app)
    exts.migrate.init_app(todos_app, exts.db)
    exts.cors.init_app(todos_app, origins="*")

    with todos_app.app_context():

        from src.services import api_bp
        todos_app.register_blueprint(api_bp)

        @todos_app.get("/")
        def entrypoint():
            return redirect("/api/")

        @todos_app.before_request
        def log_entry():
            todos_app.logger.debug("Demande de traitement")

        @todos_app.teardown_request
        def log_exit(exc):
            todos_app.logger.debug(
                "Traitement de la demande terminé", exc_info=exc
            )

        if not todos_app.debug:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/logging.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)

            todos_app.logger.addHandler(file_handler)
            todos_app.logger.setLevel(logging.INFO)
            todos_app.logger.info("running todos app")

        return todos_app
