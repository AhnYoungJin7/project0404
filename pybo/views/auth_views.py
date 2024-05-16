from flask import Flask, Blueprint, url_for, render_template, request, flash, session, g
from werkzeug.utils import redirect
from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import functools

bp = Blueprint("auth", __name__, url_prefix="/auth")

def required_login(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if g.user is None:
            to = request.url if request.method=="GET" else ''
            return redirect(url_for('auth.login', to=to))
        
        return func(*args, **kwargs)

    return wrapper

@bp.route("/checkusername/<username>")
def check_user_name(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return str(1)
    else:
        return str(-1)



# @bp.before_app_request # 모든 요청에 들어오더라도 반드시 먼저 실행하는 코드
# def set_g():
#     user_id = session.get("user_id")
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = User.query.get(user_id)

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))

@bp.route("/login", methods = ("GET", "POST"))
def login():
    form = UserLoginForm()

    if request.method == "POST" and form.validate_on_submit():
        error = None

        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 회원입니다."
        elif check_password_hash(user.password, form.password.data):
            error = "비밀번호가 틀렸습니다."

        if error is None:
            session.clear()
            session['user_id'] = user.id

            to = request.args.get("to", "")

            if to:
                return redirect(to)
            else:
                return redirect(url_for("main.index"))
        
        flash(error)

    return render_template("auth/login.html", form=form)

@bp.route("/signup", methods=("GET", "POST"))
def signup():
    form = UserCreateForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        user2 = User.query.filter_by(email=form.email.data).first()

        if user2:
            flash("이미 존재하는 이메일입니다.")
            return render_template("auth/signup.html", form=form)

        if not user:
            username = form.username.data
            password = generate_password_hash(form.password1.data)
            email = form.email.data

            user = User(username=username, password=password, email=email)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for("main.index"))
        else:
            flash("이미 존재하는 사용자입니다.")

    return render_template("auth/signup.html", form=form)