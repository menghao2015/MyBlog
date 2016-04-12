import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_POOL_RECYCLE = 10
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <lucky__menghao@163.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'menghao_92@163.com'
	FLASKY_POSTS_PER_PAGE = 10
	FLASKY_COMMENTS_PER_PAGE = 10
	SSL_DISABLE = True
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

	@staticmethod
	def init_app(apl):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
				'mysql://root:redhat@192.168.0.30/data_dev'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
				'mysql://root:redhat@192.168.0.30/data_test'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
				'mysql://root:redhat@192.168.0.30/data_dev'
	
	@classmethod
	def init_app(cls, apl):
		Config.init_app(apl)
		
		# email errors to the administrators
		import logging
		from logging.handlers import SMTPHandler
		credentials = None
		secure = None
		if getattr(cls, 'MAIL_USERNAME', None) is not None:
			credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
		if getattr(cls, 'MAIL_USE_TLS', None):
			secure = ()
		mail_handler = SMTPHandler(
			mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
			fromaddr=cls.FLASKY_MAIL_SENDER,
			toaddrs=[cls.FLASKY_ADMIN],
			subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
			credentials=credentials,
			secure=secure)
		mail_handler.setLevel(logging.ERROR)
		apl.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
	@classmethod
	def init_app(cls, apl):
		ProductionConfig.init_app(apl)

		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.WARNING)
		apl.logger.addHandler(file_handler)
		SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

		from werkzeug.contrib.fixers import ProxyFix
		apl.wsgi_app = ProxyFix(apl.wsgi_app)



config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'heroku': HerokuConfig,

	'default': DevelopmentConfig
}
