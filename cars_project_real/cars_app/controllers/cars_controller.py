from flask.helpers import flash
from cars_app import app
from flask import render_template, redirect, request, session
from cars_app.models.car import Car
from cars_app.models.user import User

# to use later for login and registration
# localhost:5000/
@app.route('/')
def index():
    return render_template('users_new.html')

##################### LOGIN IN #############################################

@app.route('/cars')
def car_dashboard():
    if not 'user_id' in session:
        flash('Must be logged in')
        return redirect ('/')
    cars = Car.get_all()
    data = {
        'id' : session['user_id']
    }
    user = User.get_one_complete(data)
    return render_template('cars_dash.html', cars = cars, user = user)

@app.route('/cars/new')
def cars_new():
    if not 'user_id' in session:
        return redirect ('/')

    return render_template('cars_new.html') #show form

@app.route('/cars/create', methods = ['POST'])
def create_car():
    if not 'user_id' in session:
        return redirect ('/')

    if not Car.validate(request.form):
        return redirect('/cars/new')
    data = {
            'color' : request.form['color'],
            'year' : request.form['year'],
            'maker_id' : request.form['maker_id'],
            'user_id' : session['user_id'],
        }
    Car.save(data)
    return redirect('/cars')

@app.route('/cars/<int:car_id>')
def car_show(car_id):
    if not 'user_id' in session:
        return redirect ('/')

    data = {
        'id' : car_id,
    }
    # car = Car.get_one(data)
    # car = Car.get_one_with_user(data)
    # car = Car.get_one_with_maker(data)
    car = Car.get_one_complete(data)
    return render_template('cars_view.html', car=car)

@app.route('/cars/<int:car_id>/edit')
def car_edit(car_id):
    if not 'user_id' in session:
        return redirect ('/')

    data = {
        'id' : car_id,
    }
    car = Car.get_one(data)
# get one car
# populate a form
    return render_template('cars_edit.html', car=car)

@app.route('/cars/<int:car_id>/update', methods = ['POST'])
def car_update(car_id):
    if not 'user_id' in session:
        return redirect ('/')

    if not Car.validate(request.form):
        return redirect(f'/cars/{car_id}/edit')
    data = {
        'id' : car_id,
        'color' : request.form['color'],
        'year' : request.form['year'],
    }
    # update the car
    Car.update(data)
    return redirect(f'/cars/{car_id}')


@app.route('/cars/<int:car_id>/destroy')
def car_destroy(car_id):
    if not 'user_id' in session:
        return redirect ('/')

    data = {
        'id' : car_id,
    }
    Car.delete(data)
    return redirect('/cars')

