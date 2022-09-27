from crypt import methods
from email.mime import image
from email.policy import default
from enum import unique
from glob import escape
from pickle import FALSE, TRUE
from sre_constants import IN
from tokenize import String
from typing import Text
from wsgiref.validate import validator
from flask import Flask, url_for, request, redirect, render_template, session, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user, LoginManager, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, IntegerField, TextAreaField, FloatField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email
from flask_wtf.file import FileField, FileAllowed , FileRequired
from flask_bcrypt import Bcrypt
import os  

app = Flask(__name__)
db = SQLAlchemy(app)
bycrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = "\xb0(I\xc3\xe3E\x84\xd6\xc9@\x13<\x1cG\xfa\xc6H)\xcc*\xbc\xd6\xf6\xa4"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=FALSE, unique=TRUE)
    password = db.Column(db.String(80), nullable=FALSE)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=TRUE)
    title = db.Column(db.String(150), nullable=FALSE, unique=TRUE)
    price = db.Column(db.Numeric(10, 2), nullable=FALSE)
    discount = db.Column(db.Integer, nullable=FALSE)
    stock = db.Column(db.Integer, nullable=FALSE)
    desc = db.Column(db.Text, nullable=FALSE)
    


class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
    submit = SubmitField("Register")


    def validate_username(self, username):
        existing_user_name = User.query.filter_by(
            username = username.data
        ).first()
        if existing_user_name:
            raise ValidationError(
                "This username already exists. Please choose a different one."
            )

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
    submit = SubmitField("Log In")

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

class AddProductForm(FlaskForm):
    title = StringField('Title', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user: 
            if bycrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('shopping_home'))
    return render_template('log_in.html', form=form)

@app.route('/home')
@login_required
def shopping_home():
    return render_template('shopping_home.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bycrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('account.html', form=form)

@app.route("/addproduct", methods=["GET", "POST"])
def addproduct():
    form = AddProductForm(request.form)
    if form.validate_on_submit():
        title = form.title.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        desc = form.description.data
        new_prod = Product(
            title = title,
            price = price,
            discount = discount,
            stock = stock,
            desc = desc
        )
        db.session.add(new_prod)
        db.session.commit()
        return redirect(url_for('addproduct'))
    else:
        return render_template('addproduct.html', form=form)
    

if __name__ == "__main__":
   app.run(debug=True)