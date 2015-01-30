from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, abort, flash
from flask.ext.login import login_required, current_user
from . import main
from .forms import StudentForm, AbstractForm
from .. import db
from ..models import Student, Abstract
#from ..email import send_email
#from ..decorators import admin_required, permission_required

@main.route('/', methods=['GET', 'POST']) 
@login_required
def index():
	"""
	name = None
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
			if current_app.config['FLASKY_ADMIN']:
				send_email(current_app.config['FLASKY_ADMIN'], 'New User',
					'mail/new_user', user=user)
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('.index'))
	"""
	#studentForm = StudentForm()
	#abstractForm = AbstractForm()
	abstract = Abstract.query.filter_by(student_id = current_user.id).first()
	

#NOT SURE WHAT'S GOING ON HERE#
	return render_template('index.html',
		abstract = abstract #, name = session.get('name'),
		#known = session.get('known', False),
		#members=somelist, current_time=datetime.utcnow()
		)

@main.route('/edit_abstract', methods=['GET', 'POST'])
@login_required
def edit_abstract():
	abstract = Abstract.query.filter_by(student_id = current_user.id).first()
	form = AbstractForm()
	if form.validate_on_submit():
		abstract.title = form.title.data
		abstract.authors = form.authors.data
		abstract.content = form.content.data
		db.session.add(abstract)
		flash('Your abstract has been updated!')
		return redirect(url_for('./', abstract=abstract))
			#title=abstract.title, authors=abstract.authors, content=abstract.content))
	form.title.data = abstract.title
	form.authors.data = abstract.authors
	form.content.data = abstract.content
	return render_template('edit_abstract.html', form=form)
"""
@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
	return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
	return "For comment moderators!"

@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	return render_template('user.html', user=user)




@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data
		user.username = form.username.data
		user.confirmed = form.confirmed.data
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data
		user.location = form.location.data
		user.about_me = form.about_me.data
		db.session.add(user)
		flash('The profile has been updated in admin mode.')
		return redirect(url_for('.user', username=user.username))
	form.email.data = user.email
	form.username.data = user.username
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id
	form.name.data = user.name
	form.location.data = user.location
	form.about_me.data = user.about_me
	return render_template('edit_profile.html', form=form, user=user)
"""




