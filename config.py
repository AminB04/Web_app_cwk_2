WTF_CSRF_ENABLED = True
SECRET_KEY = 'a-very-secret-elephant'

SESSION_COOKIE_SECURE = True

import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
