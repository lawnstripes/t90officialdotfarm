from app import db
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime
from sqlalchemy import func


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = sha256.hash(password)

    def verify_password(self, password):
        return sha256.verify(password, self.password_hash)

    def __repr__(self):
        return f'<User {self.username}>'


class Farm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitch_user = db.Column(db.String(64), index=True)
    farm_date = db.Column(db.DateTime, default=datetime.utcnow())
    farm_cnt = db.Column(db.Integer)
    __table_args__ = (db.Index('farms_date_cnt_ix', farm_date, farm_cnt),)

    @staticmethod
    def get_farm_cnt():
        sum = Farm.query.with_entities(func.sum(Farm.farm_cnt))
        return sum.scalar()
