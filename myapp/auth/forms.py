from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(Form):
	email = StringField('email', validators=[Required(),Length(1,64), Email()])
	password = PasswordField('password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')


class RegistrationForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	username = StringField('Username', validators=[Required(), Length(1,64),
							Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'can use charcter,number, underline dot')])
	password = PasswordField('Password', validators=[Required(),EqualTo('password2', 'password must match')])
	password2 = PasswordField('Confirmed', validators=[Required()])
	submit = SubmitField('register')

	def validate_email(self,field):
		email = User.query.filter_by(email=field.data).first()
		if email is not None:
			raise ValidationError('The email has been registered')

	def validate_username(self,field):
		username = User.query.filter_by(username=field.data).first()
		if username is not None:
			raise ValidationError('The username has been use')

class ChangePasswdForm(Form):
	old_password = PasswordField('old_password', validators=[Required()])
	new_password = PasswordField('Password', validators=[Required(), EqualTo('new_password2', 'password must match')])
	new_password2 = PasswordField('Password', validators=[Required()])
	submit = SubmitField('submit')

class ResetPasswdEmailForm(Form):
	email = StringField('Input Email', validators=[Required(), Length(1, 64), Email()])
	submit = SubmitField('submit')

class ResetPasswdForm(Form):
	email = StringField('Input Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('New Password', validators=[Required(), EqualTo('password2', 'Password must match')])
	password2 =PasswordField('Confirmed', validators=[Required()])
	submit = SubmitField('submit')

	def validate_email(self, field):
		if  User.query.filter_by(email=field.data).first() is None:
			raise ValidationError('Unkown email')

class ChangeEmailForm(Form):
	password = PasswordField('password', validators=[Required()])
	email = StringField('new_email', validators=[Required(), Length(1, 64), Email()])
	submit = SubmitField('submit')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('The email has been use')



