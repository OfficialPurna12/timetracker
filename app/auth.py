from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.forms import LoginForm, RegisterForm
from app.models import User
from app import mongo

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(mongo.db, form.email.data)
        if user and User.verify_password(user['password_hash'], form.password.data):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        if User.find_by_email(mongo.db, form.email.data):
            flash('Email already registered', 'error')
        else:
            User.create_user(mongo.db, form.email.data, form.password.data, form.name.data)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))