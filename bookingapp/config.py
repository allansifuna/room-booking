import os
import secrets


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'kdhjgvfcmvyugdiqygiqebudb'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'roombooking.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
