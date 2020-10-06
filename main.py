# Reference: https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask


import flask
from flask import request, redirect, flash, url_for, abort

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import imghdr
import os

from python.dlmodel import Model

from werkzeug.utils import secure_filename

# # BW below is meant to be simple
app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'static/uploads'

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return flask.render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        model = Model()
        # BW for testing
        # return filename
        return flask.render_template("index.html", token=model.runInference(filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)




# UPLOAD_FOLDER = '/tmp/'
# ALLOWED_EXTENSIONS = set(['txt','jpg', 'png'])

# app = flask.Flask("__main__")

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route("/", methods=["GET", "POST"])
# def my_index():
#     if request.method == 'POST':
# # #         # for filename, file in request.files.items():
# # #         #     name = request.files[filename].name
# # #         # if 'file' not in request.files:
# # #         #     flash("No file part")
# # #         #     return redirect(request.url)
#         model = Model(request.files["image"])
#         # return flask.render_template("index.html", token=model.runInference())
# #         # BW below for testing the request contains the file
# #         # return flask.render_template("index.html", token=request.method)
# #         # return flask.render_template("index.html", token=request.__dict__.items())
#         return flask.render_template("index.html", token=request.files.get("image").filename)

# # #         # BW USE BELOW AS DEFAULT
# # #         # model = Model()
# # #         # return flask.render_template("index.html", token=model.runInference())
#     else:
#         return flask.render_template("index.html")
# # @app.route("/", methods=["GET", "POST"])
# # def upload_image():

# #     if request.method == "POST":

# #         if 'file' not in request.files:
# #             flash("No file part")
# #             return redirect(request.url)
# #         file = request.files['file']
# #         if file.filename == '':
# #             flash('No selected file')
# #             return redirect(request.url)
# #         if file and allowed_file(file.filename):
# #             filename = secure_filename(file.filename)
# #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# #             flash('File uploaded!', 'success')

# #     model = Model(image)
# #     return flask.render_template("index.html", token=model.runInference())

    

# # @app.route('/', methods=['POST'])
# # def upload_file():
# #     uploaded_file = request.files['file']
# #     # if uploaded_file.filename != '':
# #     #     uploaded_file.save(uploaded_file.filename)
# #     # return redirect(url_for('index'))
# #     model = Model(uploaded_file)
# #         token=model.runInference()

# # @app.route('/', methods=['GET', 'POST'])
# # def my_index():
# #     for filename, file in request.files.items():
# #         name = request.files[filename].name
# #         print(name)
# #     if request.method == 'POST':
# #         uploaded_file = request.files[{file}]
# #         if uploaded_file.filename != '':
# #             model = Model(uploaded_file)
# #         #     uploaded_file.save(uploaded_file.filename)
# #         # return redirect(url_for('index'))
# #         return flask.render_template('index.html', token=model.runInference())
# #     else:
# #         return flask.render_template('index.html')



app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))