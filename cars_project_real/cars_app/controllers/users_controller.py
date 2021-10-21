from cars_app import app
from flask import render_template, redirect, request, session
from cars_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/users')
def user_dashboard():
    users = User.get_all()
    return render_template('users_dash.html', users=users)

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    
    # TODO do we need data???
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash,
        }
    user_id = User.save(data)
    # TODO Login user --- adding user_id to Session
    session['user_id'] = user_id
    return redirect('/cars')

@app.route('/login', methods = ['POST'])
def login():
    # Validate that data
    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        'email' : request.form['email']
    }
    user = User.get_one_by_email(data)
    session['user_id'] = user.id
    return redirect('/cars')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


#################################### ONLY LOGGED IN USERS HERE ########################################


@app.route('/users/<int:user_id>')
def user_show(user_id):
    if not 'user_id' in session:
        return redirect ('/')
    data = {
        'id' : user_id,
    }
    user = User.get_one_complete(data)
    return render_template('users_view.html', user=user)