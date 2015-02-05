from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, RadioField, TextAreaField, SelectField, HiddenField, IntegerField, FormField, validators
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Student, Abstract, Publication, Award

class StudentForm(Form):
	studenttitle = RadioField('Your title: ', choices=[('','N/A'),('MD/PhD','MD/PhD'),('PhD','PhD'),('MD','MD')], validators=[validators.optional()])
	department_std = StringField('Department you belong to: ',[validators.optional()])
	advisorname1 = StringField('Name and title of your primary advisor </br>[format: Jane Michelle Doe, or Jane M Doe] : ',[validators.optional()])
	advisortitle1 = RadioField('Primary advisor\'s title: ', choices=[('MD/PhD','MD/PhD'),('PhD','PhD'),('MD','MD')], validators=[validators.optional()])
	department_adv1 = StringField('Primary advisor\'s primary appointment department: ',[validators.optional()])
	advisorname2 = StringField('Name and title of your secondary advisor </br>[format: John Michael Doe, or John M Doe] : ', [validators.optional()])
	advisortitle2 = RadioField('Secondary advisor\'s title: ', choices=[('MD/PhD','MD/PhD'),('PhD','PhD'),('MD','MD')], validators=[validators.optional()])
	department_adv2 = StringField('Secondary advisor\'s primary appointment department: ',[validators.optional()])
	submit = SubmitField('Confirm your profile')

class AbstractForm(Form):
	title = StringField('*Abstract Title: ', [validators.required()])
	eventname = HiddenField('Event: 2015 Second Look')
	authors = TextAreaField('*List of Authors [format: Janie Doe, Johnnie M Doe, etc...] : ', [validators.required()])
	content = TextAreaField('*Content [word count needs to be 250 or less] : ', [validators.required()])
	presen_type = SelectField('*Presentation Type:', choices=[('poster','poster'), ('oral', 'oral')])
	submit = SubmitField('Submit')

	def validate_content(self, field):
		text = field.data
		count = len(text.split(" "))
		if count > 250:
			raise ValidationError('Abstract cannot be more than 250 words. You currently have %d words.' % count)

class PublicationForm(Form):
	title = StringField('*Publication Title: ', [validators.required()])
	authors = TextAreaField('*List of Authors [format: Janie Doe, Johnnie M Doe, etc...] : ', [validators.required()])
	journal = StringField('*Journal name: ', [validators.required()])
	pub_year = IntegerField('*Publication year: ', [validators.required()])
	doi = StringField('DOI(optional): ',[validators.optional()])
	submit = SubmitField('Submit')

class AwardForm(Form):
	award_title = StringField('*Title of award: ', [validators.required()])
	date = StringField('*Date(year) awarded: ', [validators.required()])
	institution = StringField('*Which institution/organization did you receive the award from?: ', [validators.required()])
	submit = SubmitField('Submit')
