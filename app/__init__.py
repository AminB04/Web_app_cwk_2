import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config.from_pyfile(os.path.join(base_dir, '../config.py'))

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

migrate = Migrate(app, db)

from .models import User, Kit
from .views import *

def setup_database():
    with app.app_context():
        db.create_all()
        if not Kit.query.first():  
            kits = [
                Kit(name="Arsenal FC Home Kit 24/25", price=70.00, kit_type="Current", image_filename="arsenal_home.jpg"),
                Kit(name="Santos Neymar Kit 2012", price=50.00, kit_type="Retro", image_filename="santos.jpg"),
                Kit(name="Italy Versace Kit (Blue)", price=40.00, kit_type="Concept", image_filename="italy.jpg")
            ]
            db.session.bulk_save_objects(kits)
            db.session.commit()
setup_database()