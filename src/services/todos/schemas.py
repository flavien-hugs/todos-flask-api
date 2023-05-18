from src.exts import ma
from .models import TodoItem


class TodoSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = TodoItem
        ordered = True
        exclude = ("_id",)

    _link = ma.Hyperlinks(
        ma.URLFor("api_bp.todos_detail", values=dict(public_id="<public_id>"))
    )


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
