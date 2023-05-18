import secrets

from src.exts import db
from src.common.models import CRUDMixin, TimestampMixin


def genID():
    return secrets.randbelow(100000)


class TodoItem(CRUDMixin, TimestampMixin):

    todo_id = db.Column(db.String(5), index=True, default=genID)
    name = db.Column(db.String(180))
    is_executed = db.Column(db.Boolean)

    def __str__(self) -> str:
        return self.name or self.todo_id

    def __repr__(self):
        return f"TodoItem({self._id}, {self.todo_id}, {self.name})"
