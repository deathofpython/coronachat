from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask_login import LoginManager, login_user, logout_user, login_required
from data import models
from data import db_session
from hashing import hash_algorythm
from make_date import make_date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/start_page', methods=['POST', 'GET'])
def start_page():
    if request.method == 'GET':
        return render_template('start_page.html', title='Welcome')
    if request.method == 'POST':
        if request.form['button'] == 'Search':
            session["id"] = request.form["id"]
            return redirect('/answer')


@app.route('/answer', methods=['POST', 'GET'])
def answer():
    if request.method == 'GET':
        database_session = db_session.create_session()
        return render_template('answer.html', title='Answer',
                               param=[session["id"],
                                      database_session.query(models.User).filter
                                      (models.User.username.ilike('%' + session["id"] + '%')), list, len])
    if request.method == 'POST':
        if request.form['button'] == 'Search':
            session["id"] = request.form["id"]
            return redirect('/answer')


@login_manager.user_loader
def load_user(user_id):
    database_session = db_session.create_session()
    return database_session.query(models.User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = models.Form()
    if request.method == 'GET':
        return render_template('login.html', title='Login', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            database_session = db_session.create_session()
            user = database_session.query(models.User).filter(models.User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                user.last_seen = 'online now'
                database_session.commit()
                login_user(user)
                return redirect('/start_page')
            else:
                return render_template('login.html', title='Login', message="Wrong login or password", form=form)
        elif request.form['button'] == 'Search':
            session["id"] = request.form["id"]
            return redirect('/answer')


@app.route('/logout/<string:username>')
@login_required
def logout(username):
    database_session = db_session.create_session()
    user = database_session.query(models.User).filter(models.User.username == username).first()
    user.last_seen = 'last seen ' + make_date()
    database_session.commit()
    logout_user()
    return redirect("/start_page")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = models.Form()
    if request.method == 'GET':
        return render_template('registration.html', title='Registration', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            database_session = db_session.create_session()
            user = models.User()
            user.username = form.username.data
            user.hashed_password = hash_algorythm(form.password.data)
            try:
                database_session.add(user)
                database_session.commit()
                return redirect('/start_page')
            except:
                return render_template('registration.html', title='Registration',
                                       message="User @" + user.username + ' already exists', form=form)
        elif request.form['button'] == 'Search':
            session["id"] = request.form["id"]
            return redirect('/answer')


@app.route('/my_profile/<string:username>', methods=['GET', 'POST'])
@login_required
def view_my_profile(username):
    database_session = db_session.create_session()
    chats = database_session.query(models.Chat).filter(models.Chat.pair.ilike("%" + username + "%"))
    if request.method == 'GET':
        return render_template('my_profile.html', title='Profile', my_chats=chats)
    if request.method == 'POST':
        if request.form['button'] == 'Search':
            session["id"] = request.form["id"]
            return redirect('/answer')


@app.route('/view_profile/<string:username>', methods=['GET', 'POST'])
def view_other_profile(username):
    if request.method == 'GET':
        return render_template('view_profile.html', title='Profile', username=username)
    if request.method == 'POST':
        if request.form['button'] == 'Search':
            session["id"] = request.form["id"]
            return redirect('/answer')


@app.route('/chat/<string:username1>&<string:username2>', methods=['POST', 'GET'])
@login_required
def start_chat(username1, username2):
    database_session = db_session.create_session()
    user1 = database_session.query(models.User).filter(models.User.username == username1).first()
    user2 = database_session.query(models.User).filter(models.User.username == username2).first()
    chatter_box = database_session.query(models.Chat).\
        filter((models.Chat.pair == user1.username + '★' + user2.username) | (models.Chat.pair == user2.username + '★'
                                                                              + user1.username)).first()
    if request.method == 'GET':
        return render_template('chat.html', title='Chat@' + username1 + '&' + username2, user=user2,
                               chat=chatter_box, function=list)
    if request.method == 'POST':
        if request.form['button'] == 'Send':
            message = request.form["msg"] + '★' + username1 + ' to ' + username2 + '★' + 'at ' + make_date() + '☆'
            if not chatter_box:
                chat = models.Chat()
                pair = user1.username + '★' + user2.username
                chat.data = ''
                chat.data += message
                chat.pair = pair
                database_session.add(chat)
            else:
                chatter_box.data += message
            database_session.commit()
            return redirect('/chat/' + user1.username + '&' + user2.username)
        elif request.form['button'] == 'Search':
            session["id"] = request.form["id"]
            return redirect('/answer')


def main():
    db_session.global_init('db/blogs.sqlite')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
