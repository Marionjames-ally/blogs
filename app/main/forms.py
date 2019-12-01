from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class BlogForm(FlaskForm):
    title= StringField('Title',validators=[Required()])
    content = TextAreaField('pitch', validators=[Required()])

    submit = SubmitField('Submit')