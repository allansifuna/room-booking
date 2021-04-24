from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bookingapp.models import User, Room, Booking
from flask_login import current_user
from wtforms_components import TimeField
from datetime import date


class UserRegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             Length(min=8), DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[
        Length(min=8), DataRequired(), EqualTo('password')])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me?')


class AddRoomForm(FlaskForm):
    room_number = StringField('Room Number', validators=[
        DataRequired()])

    def validate_room_number(self, room_number):
        room = Room.query.filter_by(room_no=room_number.data).first()
        if room:
            raise ValidationError(
                'Room already exists!.')


class BookRoomForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    room_number = StringField('Room Number')
    start_time = TimeField('Start', format="%H:%M")
    end_time = TimeField('End', format="%H:%M")

    def validate_room_number(self, room_number):
        room = Room.query.filter_by(room_no=room_number.data).first()
        today = date.today()
        bookings = Booking.query.filter_by(
            room_id=room.id, booking_date=today).all()
        for booking in bookings:
            if self.start_time.data >= self.end_time.data or \
                    self.start_time.data <= booking.start_time and booking.end_time <= self.end_time.data or \
                    booking.start_time <= self.start_time.data <= booking.end_time or \
                    booking.start_time <= self.end_time.data <= booking.end_time:
                raise ValidationError(
                    'Room is already Booked!.')


class EditBookingForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    room_number = StringField('Room Number')
    start_time = TimeField('Start', format="%H:%M")
    end_time = TimeField('End', format="%H:%M")

    def validate_room_number(self, room_number):
        room = Room.query.filter_by(room_no=room_number.data).first()
        today = date.today()
        bookings = Booking.query.filter_by(
            room_id=room.id, booking_date=today).all()
        for booking in bookings:
            if self.start_time.data >= self.end_time.data or \
                    self.start_time.data <= booking.start_time and booking.end_time <= self.end_time.data or \
                    booking.start_time <= self.start_time.data <= booking.end_time or \
                    booking.start_time <= self.end_time.data <= booking.end_time:
                raise ValidationError(
                    'Room is already Booked!.')


class FilterBookingForm(FlaskForm):
    start_time = TimeField('Start', format="%H:%M")
    end_time = TimeField('End', format="%H:%M")


class DeleteRoomForm(FlaskForm):
    room_number = StringField('Room Number', validators=[
        DataRequired()])

    def validate_room_number(self, room_number):
        room = Room.query.filter_by(room_no=room_number.data).first()
        if Room.is_booked(room.id) == "Booked":
            raise ValidationError(
                'Cannot Delete a booked room!.')
