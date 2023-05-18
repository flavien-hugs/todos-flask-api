import uuid
import secrets
from datetime import datetime

from src.exts import db


class CRUDMixin(object):

    __table_args__ = {"extend_existing": True}

    _id = db.Column(
        db.Integer,
        unique=True,
        index=True,
        nullable=False,
        primary_key=True
    )
    public_id = db.Column(db.String(60), index=True, default=lambda: str(uuid.uuid4()))

    @classmethod
    def get_by_id(cls, _id):
        if any(
            (isinstance(_id, str) and _id.isdigit(), isinstance(_id, (int, float))),
        ):
            return cls.query.get(int(_id))
        return None

    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def remove(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class TimestampMixin(db.Model):

    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())
