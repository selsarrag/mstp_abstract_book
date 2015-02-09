from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import Student 
from ..email import send_email
from .forms import LoginForm #, RegistrationForm, PasswordUpdateForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user_by_email = Student.query.filter_by(bcm_email=form.bcm_email.data).first()
		user_by_id = Student.query.filter_by(bcm_id=form.bcm_id.data).first()
		if user_by_email is not None and user_by_id is not None and user_by_email == user_by_id:
			user = Student.query.filter_by(bcm_email=form.bcm_email.data).first()
			login_user(user, form.remember_me.data)
			return redirect(url_for('main.index'))
		flash('Invalid email address or student ID.')
	return render_template('/auth/login.html', form=form, current_user=current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('auth.login'))

@auth.route('/doshaburidemokamawanaito')
@login_required
def send_introduction():
	everyone = Student.query.all()
	for x in everyone:
		send_email(x.email,'Sign in and add your profile and abstract', 
					'mail/login_info',student=x)
	flash('Emails have been sent to all students')
	return redirect(url_for('main.admin_area_view'))





