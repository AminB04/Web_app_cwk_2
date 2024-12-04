from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    favourites = db.relationship('Kit', secondary='user_favourites', backref=db.backref('favourited_by', lazy='dynamic'))
    basket_items = db.relationship('Kit', secondary='user_basket', backref=db.backref('in_baskets_of', lazy='dynamic'))

# Kit model
class Kit(db.Model):
    __tablename__ = 'kit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    kit_type = db.Column(db.String(50), nullable=False)
    image_filename = db.Column(db.String(120), nullable=False)
    stock_level = db.Column(db.Integer, default=2)

# Association table for User and Kit - Favourites
user_favourites = db.Table('user_favourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('kit_id', db.Integer, db.ForeignKey('kit.id'), primary_key=True)
)

# Association table for User and Kit - Basket
user_basket = db.Table('user_basket',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('kit_id', db.Integer, db.ForeignKey('kit.id'), primary_key=True)
)
