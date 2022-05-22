from flask import Flask
from flask import render_template, redirect, url_for, request, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import json
import time
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # 数据库文件
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True  # 每次请求结束后都会自动提交数据库中的变动.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Set the secret key to some random bytes.
db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(120), unique=False)
  bestStep = db.Column(db.Integer, unique=False)
  imgPath  = db.Column(db.String(200), default="../static/img/0.png")

  def __init__(self, name, email, password=None, bestStep=10, imgPath = "../static/img/0.png"):
    self.name = name
    self.email = email
    self.password = password
    self.bestStep = bestStep
    self.imgPath = imgPath

  def __repr__(self):
    return '<User %r>' % self.name

  def toDict(self):
      return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

# @app.before_first_request
# def create_db():
#   db.create_all()
#   admin = User('admin', 'admin@163.com', "admin123")
#   db.session.add(admin)
#   guestes = [
#         User('guest1', 'guest1@qqcom', password=None, bestStep=20 ,imgPath="../static/img/0.png"),
#         User('guest2', 'guest2@gmail.com', password=None, bestStep=50,imgPath="../static/img/1.png"),
#         User('guest3', 'guest3@email.com', password=None, bestStep=20,imgPath="../static/img/15.png"),
#         User('guest4', 'guest4@example.com', password=None, bestStep=60,imgPath="../static/img/28.png"),
#         User('guest6', 'guest6@example.com', password=None, bestStep=25,imgPath="../static/img/29.png"),
#         User('guest7', 'guest7@example.com', password=None, bestStep=15,imgPath="../static/img/15.png"),
#         User('guest8', 'guest8@example.com', password=None, bestStep=5,imgPath="../static/img/0.png"),
#         User('guest9', 'guest9@example.com', password=None, bestStep=10,imgPath="../static/img/0.png"),
#   ]
#   db.session.add_all(guestes)
#   db.session.commit()

def valid_user_name(name):
    pass

def valid_password(possword):
    pass




@app.route('/')
@app.route('/index/')
def index():
    users = User.query.order_by(User.bestStep.desc()).limit(7).all()
    infolist = []
    index = 0
    now_time = time.strftime('%a, %B %d,%Y', time.localtime(time.time()))
    for item in users:
        index += 1
        infolist.append({"id": str(index), "name": item.name, "score": item.bestStep, "img": item.imgPath})
    return render_template('game.html', infolist=infolist, now_time=now_time)

@app.route('/list/')
def list():
    users = User.query.order_by(User.bestStep.desc()).limit(7).all()
    infolist = []
    index = 0
    for item in users:
        index += 1
        infolist.append({"id": str(index), "name": item.name, "score": item.bestStep, "img": item.imgPath})
    return render_template('list.html', infolist=infolist)

@app.route('/login/', methods=['GET', 'POST'])
def login(name=None):
    if request.method == 'POST':
        if session is None:
            return redirect(url_for('/'))
        else:
            request_body = json.loads(request.data)
            login_user = User.query.filter_by(name=request_body['userName'],
                                              password=request_body['password']).first()
            if login_user is None:
                return jsonify(status=1, message='password_update_error')
            else:
                session.update({'user': login_user.toDict()})  # update user in to session
                return jsonify(status=0, message='login success')
    return render_template('login.html', name=name)


@app.route('/signIn/', methods=['GET', 'POST'])
def signIn(name=None):
    if request.method == 'POST':
        request_body = json.loads(request.data)
        user_name = request_body['userName']
        email = request_body['email']
        paasword = request_body['password']
        find_exit_user = User.query.filter_by(email=email).first()
        if find_exit_user:
            return jsonify(status=1, message='user exit!')
        else:
            db.session.add(User(name=user_name, email=email, password=paasword,
                                bestStep=0))
            return jsonify(status=0, message='add success')
    if request.method == 'GET':
        return render_template('signIn.html', name=name)


@app.route('/checklogin/')
def checklogin():
    if session.get('user') is None:
        return jsonify(status=3, message='not login')
    else:
        user = session.get('user')
        login_user = User.query.filter_by(name=user['name'],
                                          email=user['email']).first()
        session.update({"user": login_user.toDict()})  # update user in to session
        return jsonify(status=0, message='user already login')


@app.route('/win/', methods=['GET', 'POST'])
def winGame():
    if session.get('user') is None:
        return jsonify(status=3, message='no login')
    else:
        if request.method == 'POST':
            request_body = json.loads(request.data)
            user_name = request_body['userName']
            email = request_body['email']
            step = request_body['step']
            db_s = db.session.query(User).filter_by(name=user_name, email=email)
            db_s.first().bestStep = int(step)
            db.session.commit()
        return jsonify(status=0,  message='update user info')


# remove the username from the session if it's there
@app.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect('/index/')

@app.route('/personalInfo/')
def personlInfo():
    if session.get('user') is None:
        return redirect("/index/")
    else:
        return render_template('personInfo.html')

@app.errorhandler(404) # page not found
def not_found(error):
    return render_template('error.html'), 404


'''
A user account and tracking feature.
A method to store puzzles and results.
A method to update and vet puzzles.
A mechanism for users to share their achievements.

'''

if __name__ == '__main__':
    app.run(host="0.0.0.0")
