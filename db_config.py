import configparser
import os

from flask import Flask
from flask_mail import Mail, Message
# from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


config = configparser.ConfigParser()
cfg = config.read('settings_dev.ini')


USER_NAME = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('POSTGRES_DB')
SECRET_KEY = os.getenv('SECRET_KEY')
APP_KEY = os.getenv('DL_APP_KEY')
SESSION_ID = os.getenv("DL_SESSION_ID")
# APP_KEY = ''
# SESSION_ID = ''
ALLOWED_EXTENSIONS = {'png', 'pdf', 'jpeg', 'jpg'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USER_NAME}:{PASSWORD}@postgres:5432/{DB_NAME}'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://fluid_dev:dluid_dev@localhost:5432/fluid_dev'
app.config['UPLOAD_FOLDER'] = '/etc/fluidbusiness/apps/fluidbusiness/files'
# app.config['UPLOAD_FOLDER'] = '/Users/basicscode/projects/chatme/apps/fluidbusiness/files'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'fluidbusinessdev@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'fluidbusinessdev@gmail.com'
app.config['MAIL_PASSWORD'] = 'Edcvfr12!'
app.secret_key = 'SECRET_KEY'
db = SQLAlchemy(app)
# cache = Cache(app)
mail = Mail(app)
migrate = Migrate(app, db)
