from cars_app.config.mysqlconnection import connectToMySQL
from cars_app.models import maker, user
from flask import flash

class Car:
    # Attributes
    def __init__(self, data): #constructor
        self.id = data['id']
        self.color = data['color']
        self.year = data['year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.maker = None
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars;"
        # results are the results from the DB
        results = connectToMySQL('cars_db').query_db(query)
        cars = []
        for car in results:
            cars.append(cls(car))
        return cars

    @classmethod
    def save(cls, data):
        query = "INSERT INTO cars (color, year, created_at, updated_at, maker_id, user_id) VALUES (%(color)s, %(year)s, NOW(), NOW(), %(maker_id)s, %(user_id)s);"
        # results are the results from the DB
        return connectToMySQL('cars_db').query_db(query, data) # return the ID of the object inserted (created)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM cars WHERE cars.id = %(id)s;"
        # results are the results from the DB
        results = connectToMySQL('cars_db').query_db(query, data)        
        return (cls(results[0]))
    

    @classmethod
    def get_one_with_maker(cls, data):
        query = "SELECT * FROM cars JOIN makers ON cars.maker_id = makers.id WHERE cars.id = %(id)s;"
        # results are the results from the DB
        results = connectToMySQL('cars_db').query_db(query, data)        
        car = (cls(results[0]))

        makers_data = {
            'id' : results[0]['makers.id'],
            'name' : results[0]['name'],
            'created_at' : results[0]['makers.created_at'],
            'updated_at' : results[0]['makers.updated_at'],
        }

        car.maker = maker.Maker(makers_data)
        return car
    
    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM cars JOIN users ON cars.user_id = users.id WHERE cars.id = %(id)s;"
        # results are the results from the DB
        results = connectToMySQL('cars_db').query_db(query, data)        
        car = (cls(results[0]))

        users_data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at'],
        }

        car.user = user.User(users_data)
        return car

    @classmethod
    def get_one_complete(cls, data):
        query = "SELECT * FROM cars JOIN users ON cars.user_id = users.id JOIN makers ON cars.maker_id = makers.id WHERE cars.id = %(id)s;"
        results = connectToMySQL('cars_db').query_db(query, data)        
        car = (cls(results[0]))
        # Add user to car.user
        users_data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at'],
        }
        car.user = user.User(users_data)

        # Add maker to car.maker
        makers_data = {
            'id' : results[0]['makers.id'],
            'name' : results[0]['name'],
            'created_at' : results[0]['makers.created_at'],
            'updated_at' : results[0]['makers.updated_at'],
        }
        car.maker = maker.Maker(makers_data)

        return car

    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET color = %(color)s, year = %(year)s, updated_at = NOW() WHERE cars.id = %(id)s;"
        return connectToMySQL('cars_db').query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars WHERE cars.id = %(id)s;"
        return connectToMySQL('cars_db').query_db(query, data) # None

    @staticmethod
    def validate(formData):
        is_valid = True

        #Validations Here
        if not formData['color'].isalpha():
            flash('Colors are made with letters... duh!')
            is_valid = False
        if len(formData['color']) < 3:
            flash('Color must be 3 Characters long. Doy.')
            is_valid = False
        if len(formData['year']) < 4:
            flash('Year must be 4 characters')
            is_valid = False
        if len(formData['year']) > 4:
            flash('What year are you in? We live in 2021, at least')
            is_valid = False

        query = 'SELECT * FROM makers WHERE id = %(maker_id)s'
        results = connectToMySQL('cars_db').query_db(query, formData)
        if not len(results) == 1:
            is_valid = False
            flash('Invalid Maker')

        return is_valid