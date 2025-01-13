from . import db
from flask_login import UserMixin
import secrets


class SystemDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server_url = db.Column(db.String(250), nullable=False, default="")
    device_name = db.Column(db.String(50), nullable=False, default="")
    device_secret = db.Column(db.String(100), nullable=False, default="")
    device_id = db.Column(db.String(10), nullable=False, default="")
    device_online_status = db.Column(db.Boolean, default=False)
    @classmethod
    def get_or_create(cls):
        details = cls.query.first()
        if details is None:
            details = cls(server_url="", device_name="", device_id="", device_secret=secrets.token_hex(32), device_online_status=False)
            db.session.add(details)
            db.session.commit()
        return details


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
