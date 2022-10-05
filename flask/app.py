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
from models import app, User, Admin, Product, bycrypt, db
from forms import LoginForm, RegistrationForm, AddProductForm

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
    

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0")

