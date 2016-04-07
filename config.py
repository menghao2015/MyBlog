import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <lucky__menghao@163.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'menghao_92@163.com'
	FLASKY_POSTS_PER_PAGE = 10
	FLASKY_COMMENTS_PER_PAGE = 10
	SSL_DISABLE = True

	@staticmethod
	def init_app(apl):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
				'mysql://root:redhat@127.0.0.1/data'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
				'mysql://root:redhat@127.0.0.1/data_test'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
				'mysql://root:redhat@127.0.0.1/data'

class HerokuConfig(ProductionConfig):
	@classmethod
	def init_app(cls, apl):
		ProductionConfig.init_app(apl)

		import loggin
		from logging import StreamHander
		file_handler = StreamHandler()
		file_handler.setLevel(loggin.WARNING)
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
