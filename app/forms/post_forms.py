"""
Forms for post creation and editing.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    """Post creation and editing form."""
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=1, max=200, message='Title must be between 1 and 200 characters')
    ])
    content = TextAreaField('Content', validators=[
        DataRequired(),
        Length(min=10, message='Content must be at least 10 characters long')
    ])
    excerpt = TextAreaField('Excerpt', validators=[
        Length(max=500, message='Excerpt must be no more than 500 characters')
    ])
    category_id = SelectField('Category', coerce=int, validators=[])
    is_published = BooleanField('Publish immediately')
    submit = SubmitField('Save Post') 