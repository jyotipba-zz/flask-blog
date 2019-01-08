from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField,
 PasswordField, SubmitField,TextAreaField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Email,  DataRequired , EqualTo, ValidationError
from my_blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    password =  PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Confirm Password', validators=[DataRequired() , EqualTo('password')] )
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken. Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already taken. Please use a different email address.')




class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password =  PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
    remember_me = BooleanField('remember me')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username= username.data).first()
            if user:
                raise ValidationError("This username is taken. Please chose another ")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email= email.data).first()
            if user:
                raise ValidationError("This email is taken. Please chose another ")


class RequestResetForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(),Email()])
    submit = SubmitField("Request Reset Password")

    def validate_email(self, email):   # second arugment should always be
      # the field we want to validate
        user = User.query.filter_by(email= email.data).first()
        if user is None:
            raise ValidationError("There is no account with this email.")


class ResetPasswordForm(FlaskForm):
    password= PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField("confirm password",
                    validators =[DataRequired(), EqualTo('password')])
    submit = SubmitField("reset password")
