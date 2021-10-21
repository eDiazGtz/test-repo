from cars_app import app
from cars_app.controllers import cars_controller, makers_controller, users_controller

if __name__=='__main__':
    app.run(debug=True)