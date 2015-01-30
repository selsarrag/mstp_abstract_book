from . import db, login_manager
from flask.ext.login import UserMixin
from flask import current_app, request
from datetime import datetime

@login_manager.user_loader
def load_user(student_email):
	return Student.query.get(int(student_email))

class Student(UserMixin, db.Model):
	__tablename__ = 'students'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	studentname = db.Column(db.String(64), index=True)
	classyear = db.Column(db.Integer, index=True) #year entered
	grade = db.Column(db.String(4), index=True) #e.g. GS2, MS3
	status = db.Column(db.Enum('active','on leave','graduated'), index=True) #active, on leave, alumni etc.
	advisorname = db.Column(db.String(64), index=True)
	department = db.Column(db.String(64), index=True)
	last_updated = db.Column(db.DateTime)
	abstracts = db.relationship('Abstract', backref='student', lazy='dynamic')
	publications = db.relationship('Publication', backref='student', lazy='dynamic')
	awards = db.relationship('Award', backref='student', lazy='dynamic')

	#def __repr__(self):
	#	return '<Student %r>' % self.email

class Abstract(db.Model):
	__tablename__ = 'abstracts'
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
	eventname = db.Column(db.String(64))
	authors = db.Column(db.Text())
	title = db.Column(db.String(128))
	content = db.Column(db.Text())
	presen_type = db.Column(db.Enum('oral','poster')) #oral vs poster

	#def __repr__(self):
	#	return '<Abstract %r>' % self.id

class Publication(db.Model):
	__tablename__ = 'publications'
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
	authors = db.Column(db.Text())
	title = db.Column(db.String(128))
	doi = db.Column(db.String())
	journal = db.Column(db.String(128))
	pub_year = db.Column(db.Integer)

class Award(db.Model):
	__tablename__ = 'awards'
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
	award_title = db.Column(db.String())
	date = db.Column(db.String())
	institution = db.Column(db.String())













