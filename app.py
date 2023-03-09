import datetime
from flask import Flask, render_template, request, flash, Markup, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from markupsafe import escape
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import *
from flask_bootstrap import Bootstrap5, SwitchField
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)  # Initialize the login manager

@login_manager.user_loader
def load_user(user_id):
    # Load and return the user from the database based on user_id
    return User.query.get(int(user_id))

@app.route('/dashboard')
@login_required
def dashboard():
    # Only logged-in users can access this route
    return render_template('dashboard.html', user=current_user)

@app.route("/")
@login_required
def index():
    return render_template('dasboard.html', utc_dt="2023-03-01")

@app.route("/sobre")
@login_required
def sobre():
    return render_template('sobre.html', utc_dt="2023-03-01")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')
