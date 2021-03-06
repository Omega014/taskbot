import os
from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user

from apps.forms import QuestionForm
from apps.models import User, Channel, Question
from apps.database import init_db, db


def create_app():
    template_dir = os.path.abspath('templates')
    app = Flask(__name__, template_folder=template_dir, static_folder="../../dist/static",)
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
    if user:
        channel = User.query.get(user).user_channel
        return redirect(url_for('mypage', user=user, channel=channel))
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET'])
def form():
    user = session.get('user_id')
    if user:
        channel = User.query.get(user).user_channel
        return redirect(url_for('mypage', user=user, channel=channel))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    user = User()
    login_user(user)
    return redirect(url_for('mypage'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route("/mypage")
def mypage():
    user = session.get('user_id')
    user_channel = User.query.get(user).user_channel
    return render_template('mypage.html', user=user, channel=user_channel)


@login_required
@app.route("/channel/<channel_id>")
def channel(channel_id):
    channel = Channel.query.get(channel_id)
    questions = Question.query.filter_by(channel_id=channel.id).all()
    return render_template('channel.html',
                           channel=channel, users=channel.users, questions=questions)


@app.route("/api/questions/<int:channel_id>")
def get_questions_api(channel_id):
    q_list = []
    for q in Question.query.filter_by(channel_id=channel_id).all():
        q_list.append({oq.id: q.title})
    return jsonify(q_list)


@app.route('/api/channels')
def get_channels_api(user_id):
    channels = User.query.get(user).user_channel
    return jsonify(channels)


@login_required
@app.route("/channel/<channel_id>/q/<question_id>/edit", methods=['POST', 'GET'])
def question_index(channel_id, question_id):

    question = Question.query.filter_by(id=question_id).one()
    form = QuestionForm(obj=question)
    form.populate_obj(question)

    if request.method == 'GET':
        return render_template('question/edit.html', form=form)

    # POST
    if form.validate_on_submit():
        # import pdb;pdb.set_trace()
        if request.form.get("is_delete"):
            db.session.delete(question)
        else:
            question.title = request.form["title"]
        db.session.commit()
    return redirect(url_for('channel', channel_id=channel_id))


@login_manager.user_loader
def load_user(user_id):
        return User()
