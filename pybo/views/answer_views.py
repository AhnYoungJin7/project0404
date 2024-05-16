from flask import Flask, Blueprint, render_template, request, url_for, flash, g
from pybo.models import Question, Answer
from datetime import datetime
from pybo import db
from werkzeug.utils import redirect
from pybo.forms import AnswerForm
from pybo.views.auth_views import required_login

bp = Blueprint("answer", __name__, url_prefix="/answer")

@bp.route("/delete/<int:answer_id>")
@required_login
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id=answer.question.id
    if g.user != answer.user:
        flash("삭제 권한이 없습니다.")
        
    else:
        db.session.delete(answer)
        db.session.commit()
        
    return redirect(url_for('question.detail', question_id=question_id))  


@bp.route("/update/<int:answer_id>", methods=("GET", "POST" ))
@required_login
def update(answer_id):
    answer = Answer.query.get_or_404(answer_id)

    if g.user != answer.user:
        flash("수정 권한이 없습니다.")
        return redirect(url_for('question.detail', question_id=answer.question.id))

    if request.method == "GET":
        form = AnswerForm(obj=answer)
    else:
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.update_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))

    return render_template('answer/answer_form.html', form=form)


@bp.route("/create/<int:question_id>", methods=("POST", ))
@required_login
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    if form.validate_on_submit(): 
        content = request.form["content"]
        create_date = datetime.now()
        user_id = request.form["user_id"]

        answer = Answer(question=question, content=content, 
                        create_date=create_date, user_id=user_id)
        

        db.session.add(answer)
        db.session.commit()
           
            # render_template(): dispatcher방식으로 포워딩됨.
            # redirect(): redirect방식으로 포워딩됨.
        return redirect(url_for("question.detail", question_id=question.id))


    return render_template("question/question_detail.html", question=question, form=form)

