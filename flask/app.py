from crypt import methods
from email.mime import image
from enum import unique
from fileinput import filename
from glob import escape
from pickle import TRUE
from unicodedata import name
from wsgiref.validate import validator
from flask import url_for, request, redirect, render_template
from flask_login import login_required, login_user, logout_user
import os  
from werkzeug.utils import secure_filename
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_login import LoginManager, UserMixin
from pickle import TRUE, FALSE
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, IntegerField, TextAreaField, FloatField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_wtf.file import FileField, FileRequired
from flask_login import current_user



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


class RegistrationForm(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={'placeholder':'Name'})
    surname = StringField(validators=[InputRequired()], render_kw={'placeholder':'Last Name'})
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
    image = FileField('Add an image for', validators=[FileRequired()])
    submit = SubmitField('Submit')

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

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

@app.route('/product/<int:id>')
@login_required
def single_page(id):
    product = Product.query.get_or_404(id)
    return render_template('single_page.html', product=product)

'''Jamal Bugti 5:29 video no. 19'''
@app.route('/home')
@login_required
def shopping_home():
    page = request.args.get('page ',1, type=int)
    products = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).paginate(page=page, per_page=8)
    return render_template('shopping_home.html', products=products)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bycrypt.generate_password_hash(form.password.data)
        new_user = User(name = form.name.data, surname = form.surname.data, username=form.username.data, password=hashed_password)
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
    return render_template('account.html')

@app.route("/addproduct", methods=["GET", "POST"])
def addproduct():
    form = AddProductForm(request.form)
    if request.method == 'POST':
        image = request.files['pic']
        if not image:
            return "Pic not uploaded", 400
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
        mimetype = image.mimetype
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
            desc = desc,
            img = image.read(),
            mimetype = mimetype,
            img_name = filename
        )
        db.session.add(new_prod)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('addproduct.html', form=form)
    
@app.route('/admin')
def admin():
    form = LoginForm()
    return render_template("admin.html", form=form)

@app.route('/admin/setup')
def admin_setup():
    form = RegistrationForm()
    return render_template("admin_setup.html", form=form)

@app.route('/addcart', methods=["POST"])
def addcart():
    try: 
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == "POST":
            DicItems = {product_id:{'name': product.id, 'price': product.price, 'discount': product.discount, 'quantity': quantity, 'image': product.img_name}}
            if 'ShoppingCart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print("This product is already in your cart")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DicItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DicItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
    

if __name__ == "__main__":
   app.run(debug=False, host="0.0.0.0")

