import os

from flask import Flask, render_template, session, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy

import apps.models
from apps.models import User
from apps.database import init_db


def create_app():
    template_dir = os.path.abspath('templates')
    app = Flask(__name__, template_folder=template_dir)
    app.config['SECRET_KEY'] = 'omega014'
    app.config.from_object('apps.config.Config')

    init_db(app)

    return app

app = create_app()


# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


def get_login_user():
    if "user_id" not in session:
        return None


@app.route("/")
def index():
    user = session.get('user_id')
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET'])
def form():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    user = User()
    login_user(user)
    return redirect(url_for('index'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
        return User()
