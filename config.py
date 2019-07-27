import os
project_dir = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    # ...
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "userdatabase.db"))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',database_file) 
    SECRET_KEY = "thisisjustaboutthemostfunillgetataandela"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    UPLOADS_DEFAULT_DEST = 'project_dir/static/img'
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/project_dir/static/img'

    UPLOADED_DEFAULT_DEST = 'project_dir/static/img'
    UPLOADED_DEFAULT_URL = 'http://localhost:5000/project_dir/static/img'