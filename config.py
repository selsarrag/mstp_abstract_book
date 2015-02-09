import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'mahotest'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	QUICKABSTRACT_MAIL_SUBJECT_PREFIX = '[MSTP Second Look] '
	QUICKABSTRACT_MAIL_SENDER = 'Abstract book admin <msasaki.a@gmail.com>'
	#FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class ProductionConfig(Config):
	DEBUG = False
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or \
		'mysql://abstract_book:mstp_abstractbook@localhost/abstract_info'


config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'default' : DevelopmentConfig
}
