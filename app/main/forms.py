from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required


class BlogForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    content = TextAreaField('quote', validators=[Required()])

    submit = SubmitField('Submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    content = TextAreaField('Add comment', validators=[Required()])
    submit = SubmitField()
    
class UpForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    content = TextAreaField('quote', validators=[Required()])

    submit = SubmitField('Submit')