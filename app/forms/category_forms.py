"""
Forms for category management.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CategoryForm(FlaskForm):
    """Category creation and editing form."""
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=1, max=50, message='Name must be between 1 and 50 characters')
    ])
    description = TextAreaField('Description', validators=[
        Length(max=500, message='Description must be no more than 500 characters')
    ])
    color = StringField('Color (hex code)', validators=[
        Length(max=7, message='Color must be a valid hex code (e.g., #FF0000)')
    ])
    submit = SubmitField('Save Category') 