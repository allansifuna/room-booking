from bookingapp import db, lm
from flask import current_app
from flask_login import UserMixin
from datetime import date


class CRUDMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50))
    l_name = db.Column(db.String(50))
    email = db.Column(db.String(40))
    password = db.Column(db.String(90))
    role = db.Column(db.String(40))
    booking = db.relationship('Booking', backref='userbooking', lazy=True)

    def __repr__(self):
        return f"<{self.fname}|{self.lname}>"

    @staticmethod
    def get_by_role(role):
        return User.query.filter_by(user_role=role)


class Room(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.String(50))
    room_booking = db.relationship('Booking', backref='roombooking', lazy=True)

    @staticmethod
    def by_id(room_id):
        return Room.query.get_or_404(room_id)

    def __repr__(self):
        return f"<{self.id}>"


class Booking(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    booking_date = db.Column(db.Date, nullable=False, default=date.today)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __repr__(self):
        return f"<{self.start_time}|{self.end_time}>"
