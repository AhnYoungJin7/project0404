from flask import Flask, Blueprint, render_template, request, send_file

bp = Blueprint("test", __name__, url_prefix="/test")
import time
import os
from datetime import datetime
import random
import string

@bp.route("/sightseeing")
def sightseeing():

    return render_template("test/관광지 안내소.html")

@bp.route("gdpark")
def gdpark():

    return render_template("test/gd_park.html")

@bp.route("/deletefile")
def deletefile():
    os.remove("pybo/static/upload/hello.js")
    return "hello"

@bp.route("/download")
def download():
    filename = request.args.get("filename")

# send_file를 import
    return send_file("./"+filename,
                     download_name=extract_origin_name(filename),
                     as_attachment=True)


@bp.route("/upload_ajax", methods=("POST", ))
def upload_ajax():

    # id = request.form.get("id")


    file = request.files["zzz"]
    filename = file.filename

    filename = make_new_name(filename)
    upload_path = makedirectory()

    path = os.path.join(upload_path, filename)

    file.save(path)

    idx = path.find("/static/upload")

    return path[idx:]

@bp.route("/upload", methods=("POST", ))
def upload():
    file = request.files["file"]
    filename = file.filename

    filename = make_new_name(filename)

    upload_path = makedirectory()   

    path = os.path.join(upload_path, filename)
    path = path.replace("\\", "/")
    file.save(path)

    idx = path.find("/static/upload")

    return path[idx:]

@bp.route("/uploadform")
def uploadform():
    return render_template("test/file_upload.html")


def extract_origin_name(filename):
    idx = filename.find("_") + 1
    idx = filename.find("_", idx)

    return filename[idx:]

def make_new_name(name):
    letters = string.ascii_lowercase

    rnd_name = [random.choice(letters) for i in range(10)]
    print(rnd_name)

    msg = "".join(rnd_name)
    name_ymdhms = datetime.now().strftime("%Y%m%d%H%M%S")

    return msg+"_"+name_ymdhms+"_"+name

def makedirectory():
    UPLOAD_DIR="pybo/static/upload"
    name_ymd = datetime.now().strftime("%Y%m%d")

    new_dir_path = os.path.join(UPLOAD_DIR, name_ymd)
    
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)
    
    return new_dir_path

@bp.route("checkid/<id>")
def checkid(id):
    return id+": test"

@bp.route("/check_id_form")
def check_id_form():
    return render_template("test/check_id.html")

def monitor(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func()
        end = time.time()

        return str(end-start)
    return wrapper

@monitor # 클로저를 만들면, 나중에 함수를 2번 호출해야 함. 
            # 2번 호출하던걸 1번만
def hello():
    for i in range(100):
        print("world")
    return "hello"

@bp.route("/deco")
def deco():
    
    return hello()


@bp.route("/child")
def child():
    return render_template("test/child.html")

@bp.route("/login")
def login():
    # 확장자가 있으면 파일
    # 확장자가 없으면 폴더
    return render_template("test/login.html")

@bp.route("/say")
def say():
    ls1 = ["a", "b", "c"]
    return render_template("test/say.html", ls1=ls1)