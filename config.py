import os
project_dir = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    # ...
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "userdatabase.db"))
    SQLALCHEMY_DATABASE_URI = database_file
    SECRET_KEY = "thisisjustaboutthemostfunillgetataandela"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')