# forms.py

from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# Roʻyxatdan oʻtish uchun FORM
class RegistrationForm(FlaskForm):
	username = StringField('Foydalanuvchi nomi', validators=[DataRequired(), Length(min=5, max=50)])
	email = EmailField('E-pochta manzili', validators=[DataRequired(), Email()])
	password = PasswordField('Parol', validators=[DataRequired()])
	confirm_password = PasswordField('Parolni tasdiqlang', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Roʻyxatdan oʻtish')

	# USERNAME-ni tekshirish uchun funksiya
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Bu foydalanuvchi nomi olingan. Boshqasini tanlang.')

	# EMAIL-ni tekshirish uchun funksiya
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Bu elektron pochta olingan. Boshqasini tanlang.')

# LOGIN uchun FORM
class LoginForm(FlaskForm):
	email = EmailField('E-pochta manzili', validators=[DataRequired(), Email()])
	password = PasswordField('Parol', validators=[DataRequired()])
	remember = BooleanField('Eslab QOL')
	submit = SubmitField('Tizimga kirish')
