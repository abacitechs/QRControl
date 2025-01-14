from . import db
from flask_login import UserMixin
import secrets
import json



class SystemDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server_url = db.Column(db.String(250), nullable=False, default="")
    device_name = db.Column(db.String(50), nullable=False, default="")
    device_id = db.Column(db.String(10), nullable=False, default="")
    device_secret = db.Column(db.String(100), nullable=False, default="")
    tenant = db.Column(db.String(50), nullable=False, default="")

    @classmethod
    def get_or_create(cls):
        details = cls.query.first()
        if details is None:
            details = cls(
                server_url="",
                device_name="",
                device_id="",
                tenant="",
                device_secret=secrets.token_hex(32)
            )
            db.session.add(details)
            db.session.commit()
        return details

    def to_dict(self):
        """
        Serialize the object into a dictionary.
        """
        return {
            "server_url": self.server_url,
            "device_name": self.device_name,
            "device_id": self.device_id,
            "device_secret": self.device_secret,
            "tenant": self.tenant
        }

    def update_redis(self):
        """
        Sync the entire object as JSON to Redis under the key 'system_info'.
        """
        try:
            redis_client.set("system_info", json.dumps(self.to_dict()))
            print(f"System details synced to Redis: {self.to_dict()}")
        except Exception as e:
            print(f"Error syncing to Redis: {e}")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
