from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, abort, flash
from flask.ext.login import login_required, current_user
from . import main
from .forms import StudentForm, AbstractForm, PublicationForm, AwardForm #, PublicationListForm
from .. import db
from ..models import Student, Abstract, Publication, Award
#from ..email import send_email
#from ..decorators import admin_required, permission_required

@main.route('/', methods=['GET', 'POST']) 
@login_required
def index():

	abstract = Abstract.query.filter_by(student_id = current_user.id).first()
	publications = Publication.query.filter_by(student_id = current_user.id).all()
	award = Award.query.filter_by(student_id = current_user.id).first()

	return render_template('index.html',
		abstract = abstract, publications = publications, award = award 
		#, name = session.get('name'),
		#known = session.get('known', False),
		#current_time=datetime.utcnow()
		)

@main.route('/edit_abstract', methods=['GET', 'POST'])
@login_required
def edit_abstract():
	if Abstract.query.filter_by(student_id = current_user.id).first() is None:
		new_abstract = Abstract(student_id=current_user.id)
		db.session.add(new_abstract)
		db.session.commit()
	abstract = Abstract.query.filter_by(student_id = current_user.id).first()
	
	form = AbstractForm()

	if form.validate_on_submit():
		abstract.title = form.title.data
		abstract.authors = form.authors.data
		abstract.content = form.content.data
		abstract.eventname = "2015 Second Look"
		abstract.presen_type = form.presen_type.data
		db.session.add(abstract)
		db.session.commit()
		flash('Your abstract has been updated!')
		return redirect(url_for('.index', abstract=abstract))
	form.title.data = abstract.title
	form.authors.data = abstract.authors
	form.content.data = abstract.content
	#form.eventname.data = abstract.eventname
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
	publication = Publication.query.filter_by(student_id = current_user.id).get_or_404(id)
	form = PublicationForm()
	
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

@main.route('/edit_awards', methods=['GET', 'POST'])
@login_required
def edit_awards():
	if Award.query.filter_by(student_id = current_user.id).first() is None:
		new_award = Award(student_id=current_user.id)
		db.session.add(new_award)
		db.session.commit()
	award = Award.query.filter_by(student_id = current_user.id).first()
	
	form = AwardForm()

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
