from cars_app.config.mysqlconnection import connectToMySQL
from cars_app.models import car
from flask import flash
from cars_app import app
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

class User:
    # Attributes
    def __init__(self, data): # Constructor -- data expected to be DICT
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cars = []

    # Methods
    @classmethod
    def get_all(cls):
        # query
        query = "SELECT * FROM users;"
        # actually query DB
        results = connectToMySQL('cars_db').query_db(query)
        # new list to append obj to
        users = []
        # for loop
        for user in results:
        # turn dicts into obj
            users.append(cls(user))
        # return new list of obj
        return users
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s,%(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('cars_db').query_db(query, data)

    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL('cars_db').query_db(query, data)
        if not results:
            return False
        else:
            return cls(results[0])

    @classmethod
    def get_one_complete(cls, data):
        query = "SELECT * FROM users LEFT JOIN cars ON cars.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('cars_db').query_db(query, data)
        user = (cls(results[0]))

        if results[0]['cars.id'] == None:
            return (cls(results[0]))
        else: 
            # Add user to car.user
            for car_dict in results:
                car_data = {
                    'id' : car_dict['cars.id'],
                    'color' : car_dict['color'],
                    'year' : car_dict['year'],
                    'created_at' : car_dict['cars.created_at'],
                    'updated_at' : car_dict['cars.updated_at'],
                }
                user.cars.append(car.Car.get_one_complete(car_data))
        return user

    @staticmethod
    def validate_registration(formData):
        is_valid = True

        #Validations Here
        
        #TODO validate user ----
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(formData['email']): 
            flash("Invalid email address!")
            is_valid = False
        # make emails unique
        # make sure a user doesn't exist with formData['email']
        e_data = {'email' : formData['email']}
        user = User.get_one_by_email(e_data)
        if user:
            flash("This email is taken")
            is_valid = False
        
        if len(formData['password']) < 8:
            flash('Passwords mustbe at least 8 characters long')
            is_valid = False

        if not formData['password'] == formData['confirm_password']:
            flash('Passwords must match')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(formData):
        is_valid = True

        #Validations Here
        # make sure a user doesn't exist with formData['email']
        e_data = {'email' : formData['email']}
        user = User.get_one_by_email(e_data)
        if not user:
            flash("Invalid Email/Password")
            is_valid = False
        
        elif not bcrypt.check_password_hash(user.password, formData['password']):
            flash('Invalid Email/Password')
            is_valid = False

        return is_valid