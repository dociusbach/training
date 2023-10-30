from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from .checks import password_complexity
from .dbmodels import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@auth.route('/Login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            pass_check = check_password_hash(user.password, password)
            if pass_check is False:
                flash(category='error', message='Incorrect Username or Password')
            else:
                flash(category='success', message='Success')
                login_user(user, remember=True)
                return redirect(url_for('location.auth_home', user=current_user))
        else:
            flash(category='error', message='Incorrect Username or Password')


    return render_template("login.html", user=current_user) 

@auth.route('/Logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login', user=current_user))

@auth.route('/Register', methods=['GET', 'POST'])

def register():
    if request.method == 'POST':
        firstName =  request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('userEmail')
        passwordFirst = request.form.get('passwordFirst')
        passwordSecond = request.form.get('passwordSecond')
        passcheck = password_complexity(passwordFirst)

        if passwordFirst != passwordSecond:
            flash(category="error", message="Passwords do not match")
        if passcheck['password_pass'] is False:
            flash(category="error", message="Password does not meet complexity requirements")
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash(category='error', message=f'Account already exists for {email} ')
            else:
                new_user = User(email=email, first_name = firstName, last_name = lastName, password = generate_password_hash(passwordFirst, method='sha256'), iconFile = 'images/default-avatar.png' )
                db.session.add(new_user)
                db.session.commit()
                flash(category = "success" ,message ="Account Created")
                return redirect(url_for('auth.login'))
        
    return render_template("register.html", user=current_user)

