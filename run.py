import logging as lg

from flask_migrate import Migrate
from flask_migrate import upgrade

from src.exts import db
from src.todos import todos_app
from src.services.todos.models import TodoItem

migrate = Migrate(todos_app, db, render_as_batch=True)


@todos_app.shell_context_processor
def make_shell_context() -> dict():
    return dict(db=db, todos=TodoItem)

@todos_app.cli.command("init_db")
def init_db():
    upgrade()
    db.create_all()
    lg.info("Database initialized !")


if __name__ == "__main__":
    todos_app.run(host="0.0.0.0")
