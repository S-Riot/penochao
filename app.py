# importing datetime module
import datetime
from datetime import datetime
import time
import os
from flask import Flask, render_template, request, flash, Markup, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from markupsafe import escape
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import Form, BooleanField, StringField, validators, ValidationError 
from wtforms import IntegerField, TextAreaField, SubmitField, RadioField, SelectField,PasswordField, EmailField
from flask_bootstrap import Bootstrap5, SwitchField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine,Column, Integer, String
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, request, flash
from flask_login import UserMixin,login_user, logout_user, login_required
# import the user model
from models import db, User
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = '3d6f45a5fc12445dbac2f59c3b6c7cb1'

# connecto to the local database
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'penochao18237.SQLite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

app.config['WTF_CSRF_ENABLED'] = True

bootstrap = Bootstrap5(app)

db.init_app(app)

# Create a database engine
engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
conn = engine.connect()
csrf = CSRFProtect(app)

login_manager = LoginManager()  # Initialize the login manager
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# classes declaration

class LoginForm(FlaskForm):
    username = StringField('username', validators=[validators.DataRequired(),validators.Length(min=4, max=20)])
    password = PasswordField('password', validators=[validators.DataRequired(),validators.Length(min=6, max=255)])
    remember = BooleanField('remember', validators=[])
    submit = SubmitField('submit')
    
    
class SignupForm(FlaskForm):
    username = StringField('username', validators=[validators.DataRequired(),validators.Length(min=4, max=20)])
    password = PasswordField('password', validators=[validators.DataRequired(),validators.Length(min=6, max=255)])
    firstname = StringField('firstname', validators=[validators.DataRequired(),validators.Length(min=2, max=255)])
    lastname = StringField('lastname', validators=[validators.DataRequired(),validators.Length(min=2, max=255)])
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    invalidCheck = BooleanField('invalidCheck', validators=[validators.DataRequired()])
    submit = SubmitField('submit')

# end of classes declaration


@login_manager.user_loader
def load_user(id_user):
    # Load and return the user from the database based on user_id
    return User.query.get(int(id_user))

@app.route('/dashboard')
@login_required
def dashboard():
    # Only logged-in users can access this route
    return render_template('dashboard.html', user=current_user)


@app.route("/")
def index():
        return render_template('index.html', utc_dt="2023-03-01")

@app.route("/sobre")
def sobre():
    return render_template('sobre.html', utc_dt="2023-03-01")

@app.route("/services")
@login_required
def services():
    return render_template('sobre.html', utc_dt="2023-03-01")

@app.route("/profile")
@login_required
def profile():
    return render_template('sobre.html', utc_dt="2023-03-01")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # process the form data
            username = form.username.data
            password = form.password.data
            remember = request.form.get('remember')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            #update the last login on the database
            curr_dt = datetime.now()
            lastlogin = int(round(curr_dt.timestamp()))
            user.lastlogin = lastlogin
            db.session.commit()
            return redirect(url_for('dashboard',user=user))
        else:
            flash('Invalid username or password.','danger')

    return render_template('login.html', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
        curr_dt = datetime.now()
        form = SignupForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None:
                flash('That username is already taken. Please choose a different one.')
                return redirect(url_for('signup'))
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None:
                flash('That email is already taken. Please choose a different one.')
                return redirect(url_for('signup'))
            datecreated = int(round(curr_dt.timestamp())) # this moment in time.
            userlevel = 10 # to-do: change status later, 0 must be full admin
            accountstatus = 1 # status available, the user can login and do whatever             
            password_hash = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password=password_hash,firstname = form.firstname.data, lastname = form.lastname.data, datecreated = datecreated, userlevel=userlevel,accountstatus = accountstatus)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('index'))
        return render_template('signup.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.close()
    return redirect("/")

# jinja template filters

@app.template_filter('date')
def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    return datetime.fromtimestamp(value).strftime(format)

if __name__ == "__main__":
    app.debug = True
    app.run()
