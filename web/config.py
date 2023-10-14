import os

class Config(object):
    UPLOAD_FILES_PATH = R'C:\Users\Dima\Desktop\Repositories\HackathonAI\web\user-tmp-files'
    ALLOWED_EXTENSIONS_VIDEO = set(['mp4', 'mov', 'MOV'])
    ALLOWED_EXTENSIONS_IMAGE = set(['png', 'jpeg', 'jpg'])

    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fpasnfok;lm23441241asfasf52903'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ################
    # Flask-Security
    ################

    SECURITY_PASSWORD_HASH = "alksbf_1052131271jn"
    SECURITY_PASSWORD_SALT = "fsdfdfskasn;f79ytasfasgag12r2134124boj"