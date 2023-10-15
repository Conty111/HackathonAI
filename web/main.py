from flask import Flask, render_template, request, redirect, send_file
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

import os

from config import Config
from filter import Filter
from handle_video import Frames

def create_app():
    app = Flask(__name__, template_folder=R"C:\Users\Dima\Desktop\Repositories\HackathonAI\web\static\templates")

    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = 2048 * 1024 * 1024
    app.config['UPLOAD_FOLDER']  = Config.UPLOAD_FILES_PATH

    return app


app = create_app()
moder = Filter('words.txt')
video_handler = Frames()

class VideoUploadForm(FlaskForm):
    video = FileField('Выберите видео', validators=[DataRequired()])


def allowed_file(filename: str, type: str) -> bool:
    if '.' in filename:
        if type == "video":
            return filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS_VIDEO
        return filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS_IMAGE


@app.route('/', methods=['GET'])
def index():
    return render_template('hello.html')


@app.route('/logo', methods=['GET', 'POST'])
def img_logo():
    if request.method == "POST":
        if moder.check(request.form['prompt']):
            return f"Сгенерированный логотип по запросу: {request.form['prompt']}"
        elif not moder.check(request.form['prompt']):
            return f"Prompt is not available"
    return render_template(R"get_logo.html")


@app.route('/banner', methods=['GET', 'POST'])
def img_banner():
    if request.method == "POST":
        if moder.check(request.form['prompt']):
            return f"Сгенерированный баннер по запросу: {request.form['prompt']}"
        elif not moder.check(request.form['prompt']):
            return f"Prompt is not available"
    return render_template(R"get_banner.html")


@app.route('/preview', methods=['GET', 'POST'])
def preview():
    if request.method == "POST":
        file = request.files['file']
        promt = request.form['description']
        start_min, start_sec = int(request.form['start_minutes']), int(request.form['start_seconds'])
        end_min, end_sec = int(request.form['end_minutes']), int(request.form['end_seconds'])
        if file and allowed_file(file.filename, type="video") and moder.check(promt):
            filename = secure_filename(file.filename)
            start_time = start_min*60 + start_sec
            end_time = end_min*60 + end_sec

            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(video_path)   
            res_dir = video_handler.save_frames(video_path, 
                                      start_time=start_time, end_time=end_time)
            image_names = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], res_dir))
            return render_template('frames.html', image_names=image_names, dirname=res_dir)
        elif not moder.check(promt):
            return f"Prompt is not available"
    return render_template("preview.html")


@app.route('/result/<dirname>/<image_name>', methods=['GET'])
def get_image(dirname, image_name):
    image_path = os.path.join(os.path.join(Config.UPLOAD_FILES_PATH, dirname), image_name)
    return send_file(image_path, mimetype='image/jpeg')


@app.route('/process_image/<dirname>/<image_name>', methods=['GET', 'POST'])
def process_image(dirname, image_name):
    img_path = os.path.join(os.path.join(Config.UPLOAD_FILES_PATH, dirname), image_name)
    for file in os.listdir(os.path.join(Config.UPLOAD_FILES_PATH, dirname)):
        if file != image_name:
            os.remove(os.path.join(os.path.join(Config.UPLOAD_FILES_PATH, dirname), file))
    return send_file(img_path)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
