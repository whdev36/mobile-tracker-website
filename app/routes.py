# routes.py

from app import app, db, bcrypt, socketio
from app.forms import RegistrationForm, LoginForm
from app.models import User

from datetime import datetime

from flask import jsonify, url_for, redirect, flash, render_template, request
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
	if not current_user.is_authenticated:  # Agar foydalanuvchi tizimga kirmagan boʻlsa
		return redirect(url_for('login'))  # LOGIN sahifasiga yoʻnaltirish 
	return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:     # Agar foydalanuvchi tizimga kirgan boʻlsa
		return redirect(url_for('home'))  # HOME sahifasiga yoʻnaltirish
	form = RegistrationForm()
	if form.validate_on_submit():
		# USER-ning parolini SHIFRLASH
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)  # USER-ni qoʻshish
		db.session.commit()   # USER-ni saqlash
		flash('Hisobingiz yaratildi! Endi siz tizimga kirishingiz mumkin.', 'success')
		return redirect(url_for('login'))  # LOGIN-ga yoʻnaltirish
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:     # Agar foydalanuvchi tizimga kirgan boʻlsa
		return redirect(url_for('home'))  # HOME sahifasiga yoʻnaltirish
	form = LoginForm()
	if form.validate_on_submit():

		# Foydlanuvchini e-pochtasi orqali tanlab olish
		user = User.query.filter_by(email=form.email.data).first()
		# Tanlab olingan foydalanuvchi-ning parolini DEKODLASH va tekshirish 
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)  # Tizimga kirish
			next_page = request.args.get('next', 'home')   # Keyingi sahifani olish
			return redirect(next_page)  # Keyingi sahifaga yoʻnaltirish
		else:
			flash('Kirish amalga oshmadi. Iltimos, elektron pochta va parolni tekshiring!', 'danger')
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()  # Tizimdan chiqish
	return redirect(url_for('login'))

@app.route('/account')
@login_required  # Tizimga kirish talabi
def account():
	return render_template('account.html')

# QURILMA MAʼLUMOTLARI
devices_data = []
@app.route('/devices', methods=['POST'])
def receive_devices():
	data = request.get_json()
	if not data:
		return jsonify({'error': 'Maʼlumot olinmadi'}), 400

	devices_data.append(data)
	return jsonify({'message': 'Maʼlumotlar muvaffaqiyatli qabul qilindi', 'received': data}), 200

@app.route('/devices', methods=['GET'])
def get_devices():
	return render_template('dashboard.html', devices=devices_data)


