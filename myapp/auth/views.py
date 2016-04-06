from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import  User
from .forms import LoginForm, RegistrationForm, ChangePasswdForm, ResetPasswdEmailForm \
					,ResetPasswdForm, ChangeEmailForm
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(url_for('main.index'))
		flash('Invalid username or password')
	return render_template('auth/login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash('you have been logout')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form=RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data, username=form.username.data,
								password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirmed Your Account', 
					'auth/confirm', user=user, token=token)
		flash('A confirmation email has been send to your mailbox')
		return redirect(url_for('.login'))
	return render_template('auth/register.html', form=form)
	
@auth.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirmation_token(token):
		flash('your accunt has been confirmed')
		return redirect(url_for('.login'))
	else:
		flash('The confirmation lick is Invalid  or  has expried')
	return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed \
			and request.endpoint[:5] != 'auth.'\
			and request.endpoint != 'static':
			return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed', methods=['GET', 'POST'])
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/re_confirm', methods=['GET', 'POST'])
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirmed Your Account', 
			'auth/confirm', current_user=current_user, token=token)
	flash('A  new confirmation email has been send to your mailbox')
#	return redirect(url_for('main.index'))
	return render_template('index.html') 


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_passwd():
	form = ChangePasswdForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.change_password(form.new_password.data)
			flash('Your accunt password has been change')
	return render_template('auth/change_passwd.html', form=form)

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_passwd_request():
	form = ResetPasswdEmailForm()
	user = User.query.filter_by(email=form.email.data).first()
	if form.validate_on_submit():
		if user is not None:
			token = user.generate_reset_passwd_token()
			send_email(user.email, 'Reset Your Password', 
				'auth/reset_passwd_request', user=user, token=token)
			flash('A  new confirmation email has been send to your mailbox')
			return redirect(url_for('.login'))
		else:
			flash('The email has not register, please check')
	return render_template('auth/receive_email.html', form=form)

@auth.route('/reset_passwd/<token>', methods=['GET', 'POST'])
def reset_passwd(token):
	form = ResetPasswdForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is  None:
			return redirect(url_for('main.index'))
		if user.reset_passwd(token, form.password.data):
			flash('Your accunt password has been reset')
			return redirect(url_for('.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/change_passwd.html', form=form)

@auth.route('/change_email_request',methods=['GET', 'POST'])
@login_required
def change_email_request():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(password=form.password.data):
			token = current_user.generate_change_email_token(form.email.data)
			send_email(form.email.data, 'Change Your Email', 
				'auth/change_email_request', user=current_user, token=token)
			flash('A  new confirmation email has been send to your mailbox')
			return redirect(url_for('main.index'))
		else:
			flash(' Invalid passowrd or email')
			return redirect(url_for('main.index'))
	return render_template('auth/change_email.html', form=form)

@auth.route('/change_email/<token>', methods=['GET', 'POST'])
@login_required
def	change_email(token):
	if current_user.change_email(token):
		flash('Your email has been update')
		return redirect(url_for('.login'))
	else:
		return redirect(url_for('main.index'))



		
