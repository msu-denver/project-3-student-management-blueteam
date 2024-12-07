'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s): Emily, Kayleen, Benjamin, Dennis, Nahum
Description: Project 3 - Student Management
'''

from flask import Flask
import os

app = Flask('Management Web App')
# app.secret_key = os.environ['SECRET_KEY']
app.secret_key = 'you will never know'

# db initialization
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# flask run
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Managements.db'
# db = SQLAlchemy(app)

# Docker compose up
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:135791@postgres:5432/authentication?client_encoding=utf8'
db.init_app(app)

# models initialization
from app import models
with app.app_context():
    db.create_all()

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User


# user_loader callback
@login_manager.user_loader
def load_user(id):
    try:
        return db.session.query(User).filter(User.id == id).one()
    except:
        return None


from app import routes
