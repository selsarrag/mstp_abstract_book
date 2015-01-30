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
	return render_template('/auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('auth.login'))
"""
@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm Your Account',
					'auth/email/confirm', user=user, token=token)
		flash('Confirmation email has been sent to you by email')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account. Thanks')
	else:
		flash('The confirmation link is invalid or has expired...')
	return redirect(url_for('main.index'))
"""
"""Before Chapter 10:Profile update ping?
@auth.before_app_request 
def before_request():
	if current_user.is_authenticated() \
			and not current_user.confirmed \
			and request.endpoint[:5] != 'auth.':
		return redirect(url_for('auth.unconfirmed'))
"""
"""
@auth.before_app_request #after Example 10-3 ping logged-in user
def before_request():
	if current_user.is_authenticated():
		current_user.ping()
		if not current_user.confirmed \
				and request.endpoint[:5] != 'auth.':
			return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous() or current_user.confirmed:
		return redirect('main.index')
	return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	user=current_user
	send_email(user.email,'Confirm Your Account', 
				'auth/email/confirm',user=user, token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('main.index'))
"""







