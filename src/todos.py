from dotenv import dotenv_values

from src import create_todos_app

env = dotenv_values(".flaskenv")

todos_app = create_todos_app(env.get("FLASK_CONFIG") or "dev")
