import time

from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Подключаемся к бд
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///about.db"
app.config['SECRET_KEY'] = 'gfdgfdkgfdjfgd7fddjfd'
db = SQLAlchemy(app)
auth_1 = False #переменная отвечающая за авторизацию
user_id=0


# Модели баз данных
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<users {self.id}>"


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500), unique=True)
    name = db.Column(db.String(500), unique=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


# функций баз данных
def init_db():
    with app.app_context():
        db.create_all()


def add_user(email, password):
    try:
        hash = generate_password_hash(password)
        u = Users(email=email, password=hash)
        db.session.add(u)
        db.session.commit()
        return True

    except Exception as e:

        db.session().rollback()

        print("Ошибка при добавлений пользователя в БД")
        print(e)
        return False
def get_comments(user_id):
    try:

        comments = Comments.query.filter_by(user_id=user_id).all()
        if len(comments)!=0:
            return comments
        else:

            return None
    except Exception as e:
        print(e)
        return None


def add_com(comment,name):
    try:
        c = Comments(comment=request.form['comment'], name=request.form['name'], user_id=user_id)
        db.session.add(c)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Ошибка при добавлений комментария в БД")
        print(e)

# РОУТЫ
@app.route('/')
def main():
    print(auth_1)
    if auth_1:

        return render_template('index.html')
    else:
        return render_template('index_not_log.html')


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        # TODO:Добавить проверку корректности входных
        result = add_user(request.form['email'], request.form['password'])
        if result:

            flash("Вы успешно зарегистрированы! Теперь вы можете оставлять комментарии")
        else:
            flash("Что-то пошло не так....Возможно вы уже зарегистрированы???")
    return render_template('reg.html')

@app.route('/add_comment',methods=['POST','GET'])
def add_comment():

    if request.method=='POST':

        add_com(request.form['comment'],request.form['name'])
        flash("Комментарий успешно добавлен")
    return redirect(url_for("main"))
@app.route('/check_my_comments')
def check_my_comments():
    comments=get_comments(user_id)
    if comments!=None:
        print(comments[0].name , comments[0].comment)
        return render_template('comments.html',comments=comments)
    else:
        return "У вас пока нет комментариев :(("
@app.route('/check_my_comments/<int:id>')
def delete_comment(id):
    try:
     Comments.query.filter_by(id=id).delete()
     db.session.commit()
    except  Exception as e:
        print(e)
    return redirect(url_for("check_my_comments"))
@app.route('/auth', methods=['POST', 'GET'])
def auth():
    global auth_1 , user_id
    if request.method == 'POST':
        try:
            user = Users.query.filter_by(email=request.form['email']).all()
            psw_hsh = user[0].password
            if check_password_hash(psw_hsh, request.form['password']):
                auth_1 = True
                user_id = user[0].id
                return redirect(url_for("main"))
            else:
                flash("Вы ввели неверный пароль")
        except Exception as e:
            print(e)
    return render_template('auth.html')


@app.route('/logout')
def logout():
    global auth_1
    global user_id
    if auth_1 == True:
        auth_1 = False
        user_id = 0
    return redirect(url_for("main"))
# init_db()

if __name__ == "__main__":
    app.run(debug=True)
