from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class searchForm(FlaskForm):
    content=StringField('search',validators=[Required()])
    submit=SubmitField('Submit')
