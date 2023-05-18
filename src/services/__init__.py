from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint("api_bp", __name__, url_prefix="/api/")

api = Api(
    api_bp,
    version="1.0",
    title="Todos Item:: API Service",
    responses={404: {"description": "Not found"}}
)

from src.services.todos.api import todos_ns  # noqa E402

api.add_namespace(todos_ns, path="/todos")
