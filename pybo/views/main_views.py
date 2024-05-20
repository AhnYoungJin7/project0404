from flask import Flask, Blueprint, render_template, request, session, g, current_app
from pybo.models import Question
from pybo.models import User


bp = Blueprint("main", __name__, url_prefix="/")

@bp.before_app_request
def set_g():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route("/")
def index():
    current_app.logger.info("info 레벨로 출력")
    page = request.args.get("page", type=int, default=1)
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)

    return render_template("question/question_list.html", question_list=question_list)
