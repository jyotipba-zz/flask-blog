from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField,TextAreaField)
from wtforms.validators import  DataRequired

class CreatePost(FlaskForm):
    Title = StringField("Title", validators=[DataRequired()])
    Body =  TextAreaField('Post', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentPostForm(FlaskForm):
        body =  TextAreaField('Comment', validators=[DataRequired()])
        submit = SubmitField('Submit')
