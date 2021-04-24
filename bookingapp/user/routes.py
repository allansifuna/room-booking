from flask import Blueprint, render_template, url_for, redirect, request, flash
from .forms import UserRegisterForm, AddRoomForm, LoginForm, BookRoomForm, DeleteRoomForm, EditBookingForm, FilterBookingForm
from flask_login import login_user, current_user, logout_user, login_required
from bookingapp import bcrypt, db
from bookingapp.models import User, Room, Booking
from datetime import date
user = Blueprint('user', __name__)


@user.route('/')
@login_required
def dashboard():
    if current_user.role != "Adminstrator":
        return redirect(url_for('user.user_dash'))
    rooms = Room.query.all()
    return render_template('home.html', rooms=rooms, Room=Room)


@user.route('/dash')
@login_required
def user_dash():
    rooms = Room.query.all()
    return render_template('index.html', rooms=rooms)


@user.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.password is not None:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('user.dashboard'))
            else:
                flash("Wrong email or Password!!", "danger")
        else:
            flash("Wrong email or Password!!", "danger")
    return render_template('login.html', form=form)


@user.route('/register', methods=["POST", "GET"])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password = form.password.data
        passw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(f_name=fname, l_name=lname, email=email, password=passw)
        user.save()
        flash('Registration Sucessful, you can sign in now', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@user.route('/add-room', methods=['POST', 'GET'])
@login_required
def add_room():
    form = AddRoomForm()
    if form.validate_on_submit():
        room = Room(room_no=form.room_number.data)
        room.save()
        flash('Room Added Sucessfully', 'success')
        return redirect(url_for('user.dashboard'))
    return render_template('addroom.html', form=form)


@user.route('/book-room/<int:room_id>', methods=['POST', 'GET'])
@login_required
def book_room(room_id):
    form = BookRoomForm()
    room = Room.query.get_or_404(room_id)

    if form.validate_on_submit():
        book = Booking(room_id=room_id, user_id=current_user.id,
                       start_time=form.start_time.data, end_time=form.end_time.data)
        book.save()
        flash('Room Booked Sucessfully', 'success')
        return redirect(url_for('user.dashboard'))
    form.first_name.data = current_user.f_name
    form.last_name.data = current_user.l_name
    form.room_number.data = room.room_no
    return render_template('bookroom.html', form=form)


@user.route('/delete-room/<int:room_id>', methods=['POST', 'GET'])
@login_required
def delete_room(room_id):
    form = DeleteRoomForm()
    room = Room.query.get_or_404(room_id)
    form.room_number.data = room.room_no
    if form.validate_on_submit():
        room.delete()
        flash('Room Successfully deleted', 'success')
        return redirect(url_for('user.dashboard'))
    return render_template('deleteroom.html', form=form)


@user.route('/view-bookings/<int:room_id>', methods=['POST', 'GET'])
@login_required
def view_bookings(room_id):
    today = date.today()
    bookings = Booking.query.filter_by(
        room_id=room_id, booking_date=today).order_by(Booking.start_time.asc())
    return render_template('viewbookings.html', bookings=bookings)


@user.route('/view-user-bookings/<int:room_id>', methods=['POST', 'GET'])
@login_required
def view_user_bookings(room_id):
    today = date.today()
    bookings = Booking.query.filter_by(
        room_id=room_id, booking_date=today, user_id=current_user.id).order_by(Booking.start_time.asc())
    return render_template('viewbookings.html', bookings=bookings)


@user.route('/delete-bookings/<int:booking_id>', methods=['POST', 'GET'])
@login_required
def delete_bookings(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.delete()
    flash("Booking deleted successfully", "success")
    return redirect(url_for('user.dashboard'))


@user.route('/edit-bookings/<int:booking_id>', methods=['POST', 'GET'])
@login_required
def edit_bookings(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = EditBookingForm()
    if form.validate_on_submit():
        booking.start_time = form.start_time.data
        booking.end_time = form.end_time.data
        db.session.commit()
        flash("Booking Edited successfully", "success")
        return redirect(url_for('user.dashboard'))
    form.first_name.data = current_user.f_name
    form.last_name.data = current_user.l_name
    form.room_number.data = booking.roombooking.room_no
    form.start_time.data = booking.start_time
    form.end_time.data = booking.end_time
    return render_template('editbooking.html', form=form)


@user.route('/filter-bookings/<int:room_id>', methods=['POST', 'GET'])
@login_required
def filter_bookings(room_id):
    form = FilterBookingForm()
    if form.validate_on_submit():
        st = form.start_time.data
        et = form.end_time.data
        bookings = Booking.query.filter_by(room_id=room_id).filter(
            Booking.start_time >= st).filter(Booking.end_time <= et).all()
        return render_template('viewbookings.html', bookings=bookings)
    return render_template('filterbookings.html', form=form)
