from flask_restx import fields
from src.services import api

todos_fields = api.model(
    "TodoItem",
    {
        "name": fields.String(required=True),
        "is_executed": fields.Boolean(default=False),
    },
)
