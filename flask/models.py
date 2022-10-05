from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_login import LoginManager, UserMixin
from pickle import FALSE, TRUE
import os

app = Flask(__name__)
db = SQLAlchemy(app)
bycrypt = Bcrypt(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "\xb0(I\xc3\xe3E\x84\xd6\xc9@\x13<\x1cG\xfa\xc6H)\xcc*\xbc\xd6\xf6\xa4"

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/uploads')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=FALSE)
    surname = db.Column(db.String, nullable=FALSE)
    username = db.Column(db.String(20), nullable=FALSE, unique=TRUE)
    password = db.Column(db.String(80), nullable=FALSE)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=TRUE)
    title = db.Column(db.String(150), nullable=FALSE, unique=TRUE)
    price = db.Column(db.Numeric(10, 2), nullable=FALSE)
    discount = db.Column(db.Integer, nullable=FALSE)
    stock = db.Column(db.Integer, nullable=FALSE)
    desc = db.Column(db.Text, nullable=FALSE)
    img = db.Column(db.Text, nullable=False)
    img_name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=TRUE)
    name = db.Column(db.String, nullable=FALSE)
    sur_name = db.Column(db.String, nullable=FALSE)
    admin_name = db.Column(db.String(20), nullable=FALSE, unique=TRUE)
    password = db.Column(db.String(80), nullable=FALSE)
