from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo
import os

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from config.py

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Forms for registration and login
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=100)])

with app.app_context():
    db.create_all()  # This will create the tables if they do not exist
    print("SQLite database and tables created successfully!")

# Routes for login, register, dashboard, and logout
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check the user in the database
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):  # Check password
            session['user_id'] = user.id  # Save user ID in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login credentials', 'danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create and save the user
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
