from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length #, Regexp, EqualTo
#from wtforms import ValidationError
#from ..models import User

class LoginForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64),
											Email()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')
