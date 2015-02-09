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
	bcm_email = db.Column(db.String(32), unique=True, index=True)
	bcm_id = db.Column(db.String(6), unique=True, index=True)
	firstname = db.Column(db.String(32), index=True)
	lastname = db.Column(db.String(32), index=True)
	studenttitle = db.Column(db.String(10), index=True)
	grade = db.Column(db.String(4), index=True) #e.g. GS2, MS3
	advisorname1 = db.Column(db.String(64), index=True)
	advisortitle1 = db.Column(db.String(10)) #, ('MD/Phd','PhD','MD'))
	advisorname2 = db.Column(db.String(64), index=True)
	advisortitle2 = db.Column(db.String(10))
	department_std = db.Column(db.String(64), index=True)
	department_adv1 = db.Column(db.String(64), index=True)
	department_adv2 = db.Column(db.String(64), index=True)
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
	presen_type = db.Column(db.String(10)) #oral vs poster
	last_updated = db.Column(db.DateTime)

	#def __repr__(self):
	#	return '<Abstract %r>' % self.id

class Publication(db.Model):
	__tablename__ = 'publications'
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
	authors = db.Column(db.Text())
	title = db.Column(db.String(128))
	doi = db.Column(db.String(32))
	journal = db.Column(db.String(128))
	pub_year = db.Column(db.String(32))

class Award(db.Model):
	__tablename__ = 'awards'
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
	award_title = db.Column(db.String(128))
	date = db.Column(db.String(32))
	institution = db.Column(db.String(64))













