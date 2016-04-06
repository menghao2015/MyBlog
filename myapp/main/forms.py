from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from ..models import Role,User


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class PostForm(Form):
	body = PageDownField('What is your mind ?', validators=[Required()])
	submit = SubmitField('Submit')

class CommentForm(Form):
	body = StringField(' ', validators=[Required()])
	submit = SubmitField('Submit')


class EditProfileForm(Form):
	name = StringField('Name', validators=[Length(0,64)])
	location = StringField('From', validators=[Length(0.64)])
	about_me = StringField('About_me', validators=[Required()])
	submit = SubmitField('submit')

class EditProfileAdminForm(Form):
	email = StringField('Email ', validators=[Required(), Length(1,64), Email()])
	username = StringField('Username', validators=[Required(), Length(1, 64), 
					Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Username must have only letters, numbers, dots or underscores')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role', coerce=int)

	name = StringField('Name ', validators=[Length(0,64)])
	location = StringField('From ', validators=[Length(0,64)])
	about_me = TextAreaField('About_me ')
	submit = SubmitField('submit')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name)
						for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if self.user.email != field.data and User.query.filter_by(email = field.data).first():
			raise ValidationError(' The email has been register ')

	def validate_username(self, field):
		if self.user.username != field.data and User.query.filtre_by(email = field.data).first():
			raise ValidationError('The username has been register ')


