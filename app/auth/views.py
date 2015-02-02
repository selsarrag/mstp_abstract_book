from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import Student 
#from ..email import send_email
from .forms import LoginForm #, RegistrationForm, PasswordUpdateForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Student.query.filter_by(email=form.email.data).first()
		if user is not None: #and user.verify_email(form.email.data):
			login_user(user, form.remember_me.data)
			return redirect(url_for('main.index'))
			#return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid user email.')
	return render_template('/auth/login.html', form=form, current_user=current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('auth.login'))



