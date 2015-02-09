from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, abort, flash, Markup
from flask.ext.login import login_required, current_user
from . import main
from .forms import StudentForm, AbstractForm, PublicationForm, AwardForm 
from .. import db
from ..models import Student, Abstract, Publication, Award
from ..email import send_email
#from ..decorators import admin_required, permission_required
import re

def needAbstract(year, cutoff=3):
    m = re.match(r'GS(\d+)', year)
    return bool(m) and int(m.group(1)) >= cutoff

@main.route('/', methods=['GET', 'POST']) 
@login_required
def index():

	abstract = Abstract.query.filter_by(student_id = current_user.id).first()
	publications = Publication.query.filter_by(student_id = current_user.id).all()
	awards = Award.query.filter_by(student_id = current_user.id).all()
	student = current_user
	need_abstract = needAbstract(student.grade)

	return render_template('index.html',
		abstract = abstract, publications = publications, awards = awards, student=student, need_abstract=need_abstract
		#, name = session.get('name'),
		#known = session.get('known', False),
		#current_time=datetime.utcnow()
		)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	student = Student.query.filter_by(id = current_user.id).first()
	form = StudentForm()
	if form.validate_on_submit():
		student.studenttitle = form.studenttitle.data
		student.advisorname1 = form.advisorname1.data
		student.advisortitle1 = form.advisortitle1.data
		student.advisorname2 = form.advisorname2.data
		student.advisortitle2 = form.advisortitle2.data
		student.department_adv1 = form.department_adv1.data
		student.department_adv2 = form.department_adv2.data
		student.department_std = form.department_std.data
		student.last_updated = datetime.utcnow()
		db.session.add(student)
		db.session.commit()
		flash('Your student profile has been updated!')
		return redirect(url_for('.index', student=student))
	form.studenttitle.data = student.studenttitle
	form.advisorname1.data = student.advisorname1
	form.advisortitle1.data = student.advisortitle1
	form.advisorname2.data = student.advisorname2
	form.advisortitle2.data = student.advisortitle2
	form.department_std.data = student.department_std
	form.department_adv1.data = student.department_adv1
	form.department_adv2.data = student.department_adv2
	return render_template('edit_profile.html', student=student, form=form)

@main.route('/edit_abstract', methods=['GET', 'POST'])
@login_required
def edit_abstract():
	
	if Abstract.query.filter_by(student_id = current_user.id).first() is None:
		new_abstract = Abstract(student_id=current_user.id)
		form = AbstractForm()
		if form.validate_on_submit():
			new_abstract.title = form.title.data
			new_abstract.authors = form.authors.data
			new_abstract.content = form.content.data
			new_abstract.eventname = "2015 Second Look"
			new_abstract.presen_type = form.presen_type.data
			new_abstract.last_updated = datetime.utcnow()
			db.session.add(new_abstract)
			db.session.commit()
			flash('Your abstract has been added!')
			return redirect(url_for('.index', abstract=new_abstract))
		form.title.data = new_abstract.title
		form.authors.data = new_abstract.authors
		form.content.data = new_abstract.content
		form.presen_type.data = new_abstract.presen_type
		return render_template('edit_abstract.html', form=form)
	
	abstract = Abstract.query.filter_by(student_id = current_user.id).first()
	form = AbstractForm()
	if form.validate_on_submit():
		abstract.title = form.title.data
		abstract.authors = form.authors.data
		abstract.content = form.content.data
		abstract.eventname = "2015 Second Look"
		abstract.presen_type = form.presen_type.data
		abstract.last_updated = datetime.utcnow()
		db.session.add(abstract)
		db.session.commit()
		flash('Your abstract has been updated!')
		return redirect(url_for('.index', abstract=abstract))
	form.title.data = abstract.title
	form.authors.data = abstract.authors
	form.content.data = abstract.content
	form.presen_type.data = abstract.presen_type
	return render_template('edit_abstract.html', form=form)

@main.route('/add_publication', methods=['GET', 'POST'])
@login_required
def add_publication():
	new_publication = Publication(student_id=current_user.id)	
	form = PublicationForm()
	if form.validate_on_submit():
		new_publication.title = form.title.data
		new_publication.authors = form.authors.data
		new_publication.doi = form.doi.data
		new_publication.journal = form.journal.data
		new_publication.pub_year = form.pub_year.data
		db.session.add(new_publication)
		db.session.commit()
		flash('Your publication has been added!')
		return redirect(url_for('.index', publication=new_publication))
	form.title.data = new_publication.title
	form.authors.data = new_publication.authors
	form.doi.data = new_publication.doi
	form.journal.data = new_publication.journal
	form.pub_year.data = new_publication.pub_year
	
	return render_template('add_publication.html', form=form)


@main.route('/edit_publications/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_publications(id):
	publication = Publication.query.get_or_404(id)
	form = PublicationForm()
	if publication.student_id == current_user.id:
		if form.validate_on_submit():
			publication.title = form.title.data
			publication.authors = form.authors.data
			publication.doi = form.doi.data
			publication.journal = form.journal.data
			publication.pub_year = form.pub_year.data
			db.session.add(publication)
			db.session.commit()
			flash('Your publication has been updated!')
			return redirect(url_for('.index', publication=publication))
		form.title.data = publication.title
		form.authors.data = publication.authors
		form.doi.data = publication.doi
		form.journal.data = publication.journal
		form.pub_year.data = publication.pub_year
		return render_template('edit_publications.html', form=form)
	return render_template('404.html')

@main.route('/delete_pub/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_pub(id):
	publication = Publication.query.get_or_404(id)
	db.session.delete(publication)
	db.session.commit
	flash('Your selected publication has been deleted!')
	return redirect(url_for('.index', publication=publication))

@main.route('/add_award', methods=['GET', 'POST'])
@login_required
def add_award():
	new_award = Award(student_id=current_user.id)	
	form = AwardForm()
	if form.validate_on_submit():
		new_award.award_title = form.award_title.data
		new_award.date = form.date.data
		new_award.institution = form.institution.data
		db.session.add(new_award)
		db.session.commit()
		flash('Your award has been added!')
		return redirect(url_for('.index', award=new_award))
	form.award_title.data = new_award.award_title
	form.date.data = new_award.date
	form.institution.data = new_award.institution
	return render_template('add_award.html', form=form)

@main.route('/edit_awards/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_awards(id):
	award = Award.query.get_or_404(id)
	form = AwardForm()
	if award.student_id == current_user.id:
		if form.validate_on_submit():
			award.award_title = form.award_title.data
			award.date = form.date.data
			award.institution = form.institution.data
			db.session.add(award)
			db.session.commit()
			flash('Your award list has been updated!')
			return redirect(url_for('.index', award=award))
		form.award_title.data = award.award_title
		form.date.data = award.date
		form.institution.data = award.institution
		return render_template('edit_awards.html', form=form)
	return render_template('404.html')

@main.route('/delete_award/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_award(id):
	award = Award.query.get_or_404(id)
	db.session.delete(award)
	db.session.commit
	flash('Your selected award has been deleted!')
	return redirect(url_for('.index', award=award))

def slacker_filter():
	missing_profiles = Student.query.filter_by(last_updated = None).all()
	students = Student.query.all()
	#example of list comprehension
	#slackers = [x for x in students if Abstract.query.filter_by(student_id=x.id).count() == 0]
	slackers = []
	for x in students:
		need_abstract = needAbstract(x.grade)
		if need_abstract and not Abstract.query.filter_by(student_id=x.id).first() :
			slackers.append(x)

	both = set(missing_profiles) & set(slackers)
	missing_p = set(missing_profiles) - both
	missing_a = set(slackers) - both
	return both, missing_p, missing_a	

@main.route('/saisokumailsender', methods=['GET'])
@login_required
def mailsender():
	#filter_result = slacker_filter()
	both = slacker_filter()[0]
	missing_p = slacker_filter()[1]
	missing_a = slacker_filter()[2]
	return render_template('saisokumailsender.html', both=both, missing_p=missing_p, missing_a=missing_a)

@main.route('/saisokumailsender/abstracts', methods=['GET'])
@login_required
def abs_list_emails():
	missing_a = slacker_filter()[2]
	email_list=[]
	for x in missing_a:
		send_email(x.email,'Submit your abstract', 
						'mail/saisoku_abstract',student=x)
		email_list.append(x.email)
	message = "Emails have been sent to the following students missing their abstract: %s" % email_list
	flash(message)
	return redirect(url_for('.admin_area_view', missing_a=missing_a))

@main.route('/saisokumailsender/profiles', methods=['GET'])
@login_required
def prof_list_emails():
	missing_p = slacker_filter()[1]
	email_list=[]
	for x in missing_p:
		send_email(x.email,'Confirm your profile', 
						'mail/saisoku_profile',student=x)
		email_list.append(x.email)
	message = "Emails have been sent to the following students missing their profile: %s" % email_list
	flash(message)
	return redirect(url_for('.admin_area_view', missing_p=missing_p))

@main.route('/saisokumailsender/both', methods=['GET'])
@login_required
def both_list_emails():
	both = slacker_filter()[0]
	email_list=[]
	for x in both:
		send_email(x.email,'Submit your abstract and confirm profile', 
						'mail/saisoku_both',student=x)
		email_list.append(x.email)
	message =  "Emails have been sent to the following students missing both fields: %s" % email_list
	flash(message)
	return redirect(url_for('.admin_area_view', both=both))


@main.route('/himitsunoadminarea')
@login_required
def admin_area_view():
	return render_template('himitsunoadminarea.html')


@main.route('/zubunuredemokamawanaito')
@login_required
def send_mass_missile():
	slacker_filter()
	both = slacker_filter()[0]
	missing_p = slacker_filter()[1]
	missing_a = slacker_filter()[2]
	email_list=[]
	for x in both:
		send_email(x.email,'Submit your abstract and confirm profile', 
						'mail/saisoku_both',student=x)
		email_list.append(x.email)
	for x in missing_a:
		send_email(x.email,'Submit your abstract', 
						'mail/saisoku_abstract',student=x)
		email_list.append(x.email)
	for x in missing_p:
		send_email(x.email,'Confirm your profile', 
						'mail/saisoku_profile',student=x)
		email_list.append(x.email)
	message = "Reminder emails have been sent out in mass to the following students: %s" % email_list
	flash(message)
	return redirect(url_for('main.admin_area_view'))
