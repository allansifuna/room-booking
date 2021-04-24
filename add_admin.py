from bookingapp import *
from bookingapp.models import *
from bookingapp import create_app
create_app().app_context().push()


def init_db():
    db.create_all()
    password = bcrypt.generate_password_hash('admin123').decode('utf-8')
    user = User(f_name='Admin', l_name='Bookingapp', password=password,
                role='Adminstrator', email='admin@bookingapp.com')
    user.save()


init_db()
