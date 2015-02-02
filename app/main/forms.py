from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, RadioField, TextAreaField, SelectField, HiddenField, IntegerField, FormField, validators
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Student, Abstract, Publication, Award

class StudentForm(Form):
	department_std = StringField('Department you belong to: ')
	advisorname = StringField('Name and title of your primary advisor [First Middle(MI) Last] : ')
	advisortitle = RadioField('Advisor\'s title: ', choices=[('MD/PhD','MD/PhD'),('PhD','PhD'),('MD','MD')])
	department_adv = StringField('Advisor\'s primary appointment department: ')
	submit = SubmitField('Submit')

class AbstractForm(Form):
	title = StringField('Abstract Title: ', [validators.required()])
	eventname = HiddenField('Event: 2015 Second Look')
	authors = TextAreaField('List of Authors [First Middle(MI) Last, First MI Last] : ', [validators.required()])
	content = TextAreaField('Content [word count needs to be 250 or less] : ', [validators.required()])
	presen_type = SelectField('Presentation Type:', choices=[('poster','poster'), ('oral', 'oral')])
	submit = SubmitField('Submit')

	def validate_content(self, field):
		text = field.data
		count = len(text.split(" "))
		if count > 250:
			raise ValidationError('Abstract cannot be more than 250 words. You currently have %d words.' % count)

class PublicationForm(Form):
	title = StringField('Publication Title: ', [validators.required()])
	authors = TextAreaField('List of Authors [First Middle(MI) Last, First MI Last] : ', [validators.required()])
	journal = StringField('Journal name: ', [validators.required()])
	pub_year = IntegerField('Publication year: ', [validators.required()])
	doi = StringField('DOI: ',[validators.optional()])
	submit = SubmitField('Submit')

"""
class PublicationListForm(Form):
	pub1 = FormField(PublicationForm)
"""
class AwardForm(Form):
	award_title = StringField('Title of award: ', [validators.required()])
	date = StringField('Date(year) awarded: ', [validators.required()])
	institution = StringField('Which institution/organization did you receive the award from?: ', [validators.required()])
	submit = SubmitField('Submit')
"""

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