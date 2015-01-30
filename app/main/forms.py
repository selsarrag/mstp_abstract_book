from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectMultipleField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Student, Abstract

class StudentForm(Form):
	name = StringField('Full Name [First MI Last]: ')
	classyear = StringField('Class Year: ')
	grade = StringField('Grade (ex. MS2, GS2 etc.): ')
	advisor = StringField('Name of your advisor [First MI Last]: ')
	department = StringField('Department: ')

	submit = SubmitField('Submit')

class AbstractForm(Form):
	title = StringField('Abstract Title: ')
	authors = TextAreaField('List of Authors: ')
	content = TextAreaField('Content: ')
	presen_type = SelectMultipleField('Presentation Type:', choices=["poster", "oral"])
	submit = SubmitField('Submit')
"""
class EditProfileForm(Form):
	name = StringField('Real name', validators=[Length(0,64)])
	location = StringField('Location', validators=[Length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')

class EditProfileAdminForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64),
											 Email()])
	username = StringField('Username', validators=[Required(), Length(1,64),
							Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
									'Usernames must have only letters, '
									'numbers, dots or underscores')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role', coerce=int) #coerce=int stores field values as integers 
	name = StringField('Real name', validators=[Length(0,64)])
	location = StringField('Location', validators=[Length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name)
							 for role in Role.query.order_by(Role.name).all()]
		self.user = user 

	def validate_email(self, field):
		if field.data != self.user.email and \
				User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if field.data != self.user.username and \
				User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use')
"""