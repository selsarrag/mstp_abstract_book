from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length #, Regexp, EqualTo
#from wtforms import ValidationError
#from ..models import User

class LoginForm(Form):
	bcm_email = StringField('BCM Email: ', validators=[Required(), Length(1,64),
											Email()])
	bcm_id = StringField('BCM ID: ', validators=[Required(), Length(1,6)])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')
