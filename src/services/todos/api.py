import logging
from http import HTTPStatus
from datetime import timedelta

from flask_restx import Resource
from flask_restx import Namespace

from .resources import todos_fields
from src.services.todos import schemas
from src.services.todos.models import TodoItem

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

todos_ns = Namespace(name="todos", validate=True)


def abort_if_todos_doesnt_exist(public_id: str):
    todo_item = TodoItem.find_by_public_id(public_id)
    if not todo_item:
        todos_ns.abort(HTTPStatus.NOT_FOUND, f"Could not find user with ID {public_id}")
    return todo_item


@todos_ns.route("/", endpoint="todos_create_list")
class TodoItemListResource(Resource):

    def get(self):
        todos = TodoItem.query.all()
        response = {"todos": schemas.todos_schema.dump(todos),}
        return response, HTTPStatus.OK

    @todos_ns.doc(
        responses={
            int(HTTPStatus.CREATED): "New todo item was successfully created.",
            int(HTTPStatus.BAD_REQUEST): "Todo item name cannot be empty.",
        },
    )
    @todos_ns.expect(todos_fields)
    def post(self):
        data = todos_ns.payload
        todo_schema = schemas.TodoSchema()
        errors = todo_schema.validate(data)

        if errors:
            response = (
                {
                    "message": "Validation failed",
                    "errors": errors,
                },
                HTTPStatus.BAD_REQUEST,
            )
        else:
            todo = TodoItem.create(**data)
            response = {
                "todo": schemas.todo_schema.dump(todo),
                "message": "Todo successfully created !",
            }
        return response, HTTPStatus.CREATED


@todos_ns.route("/<public_id>/", endpoint="todos_detail")
@todos_ns.param("public_id", "The todos item identifier")
class TodoItemDetailResource(Resource):

    @todos_ns.doc(
        responses={
            int(HTTPStatus.NOT_FOUND): "Todo not found",
        }
    )
    def get(self, public_id):
        todo = abort_if_todos_doesnt_exist(public_id)
        response = {"todo": schemas.todo_schema.dump(todo)}
        return response, HTTPStatus.OK

    @todos_ns.doc(
        responses={
            int(HTTPStatus.NOT_FOUND): "Todo not found",
            int(HTTPStatus.OK): "Todo update successfully"
        },
    )
    @todos_ns.expect(todos_fields)
    def patch(self, public_id):
        todo = abort_if_todos_doesnt_exist(public_id)

        data = todos_ns.payload
        todo_schema = schemas.TodoSchema(partial=True)
        errors = todo_schema.validate(data)
        if errors:
            response = (
                {
                    "message": "Validation failed",
                    "errors": errors,
                },
                HTTPStatus.BAD_REQUEST,
            )
        else:
            todo_item = TodoItem.update(todo, data)
            todo.save()
            response = {
                "todo": schemas.todo_schema.dump(todo),
                "message": "Todo update successfully",
            }
        return response, HTTPStatus.OK

    @todos_ns.doc(
        responses={
            int(HTTPStatus.NOT_FOUND): "Todo not found",
            int(HTTPStatus.NO_CONTENT): "Todo deleted successfully"
        }
    )
    def delete(self, public_id):
        todo = abort_if_todos_doesnt_exist(public_id)
        todo.remove()
        response = {
            "message": "Todo deleted successfully",
        }
        return response, HTTPStatus.NO_CONTENT
