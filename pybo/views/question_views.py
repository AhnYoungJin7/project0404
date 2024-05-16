from flask import Flask, Blueprint, render_template, request, url_for, g, flash
from pybo.models import Question
from pybo.forms import QuestionForm
from werkzeug.utils import redirect 
from datetime import datetime 
from pybo import db 
from pybo.forms import AnswerForm
import time
from pybo.views.auth_views import required_login
from pybo.views.test_views import extract_origin_name, make_new_name, makedirectory
import os

bp = Blueprint("question", __name__, url_prefix="/question")

@bp.route("/delete/<int:question_id>")
@required_login
def delete(question_id):
    question = Question.query.get_or_404(question_id)

    if g.user != question.user:
        flash("삭제 권한이 없습니다.")
        return redirect(url_for("question.detail", question_id=question_id))
    
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question.index'))


@bp.route("/update/<int:question_id>", methods=('GET', 'POST'))
@required_login
def update(question_id):
    question = Question.query.get_or_404(question_id)
    
    if g.user != question.user:
        flash("수정권한이 없습니다.")
        return redirect(url_for('question.detail', question_id=question_id))
    
    if request.method == "POST":
        form = QuestionForm()

        if form.validate_on_submit():

            form.populate_obj(question)
            question.update_date = datetime.now()

            del_img = request.form.get("del_img") #================================시작
            
            if del_img == "-1": 
                
                delete_filename = form.file_path.data

                if delete_filename:
                    delete_file_path = "pybo"+ delete_filename
                    os.remove(delete_file_path)

                question.file_path=""

                

            file = request.files["file"]
            
            if file.filename:
                delete_filename = form.file_path.data
                

                if delete_filename:
                    delete_file_path = "pybo"+ delete_filename
                    os.remove(delete_file_path)

                filename = file.filename
                filename = make_new_name(filename)
                upload_path = makedirectory()
                path = os.path.join(upload_path, filename)

                file.save(path)

                idx = path.find("/static/upload")
                file_path = path[idx:]

                question.file_path = file_path #================================끝         

            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))

    else:
        form = QuestionForm(obj=question)

    return render_template("question/question_update_form.html", form=form)


@bp.route("/create", methods=('GET', 'POST'))
@required_login
def create():
    form = QuestionForm()

    if request.method == 'POST' and form.validate_on_submit():
        subject = form.subject.data 
        content = form.content.data 
        create_date = datetime.now()
        user_id = form.user_id.data

        file = request.files["file"]
        filename = file.filename

        filename = make_new_name(filename)

        upload_path = makedirectory()

        path = os.path.join(upload_path, filename)
        path = path.replace("\\", "/")

        file.save(path)

        idx = path.find("/static/upload")

        file_path = path[idx:]


        question = Question(subject=subject, content=content,
                            create_date=create_date, user_id=user_id,
                            file_path=file_path)
        
        db.session.add(question)

        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("question/question_form.html", form=form)

@bp.route("/detail/<int:question_id>")
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get(question_id)
    return render_template("question/question_detail.html", 
                           question=question, form=form)

@bp.route("/list")
def index():
    page = request.args.get("page", type=int, default=1)
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)

    return render_template("question/question_list.html", question_list =question_list )