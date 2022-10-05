from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, IntegerField, TextAreaField, FloatField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_wtf.file import FileField, FileRequired
from flask_login import current_user
from models import User 

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

