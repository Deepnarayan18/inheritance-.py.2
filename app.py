import logging
from flask import Flask, render_template, request

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        return f"Make: {self.make}, Model: {self.model}, Year: {self.year}"

class Car(Vehicle):
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def display_info(self):
        return super().display_info() + f", Number of doors: {self.num_doors}"

class Motorcycle(Vehicle):
    def __init__(self, make, model, year, has_sidecar):
        super().__init__(make, model, year)
        self.has_sidecar = has_sidecar

    def display_info(self):
        return super().display_info() + f", Has sidecar: {'Yes' if self.has_sidecar else 'No'}"

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            car_make = request.form['car_make']
            car_model = request.form['car_model']
            car_year = int(request.form['car_year'])
            car_num_doors = int(request.form['car_num_doors'])

            motorcycle_make = request.form['motorcycle_make']
            motorcycle_model = request.form['motorcycle_model']
            motorcycle_year = int(request.form['motorcycle_year'])
            motorcycle_has_sidecar = request.form.get('motorcycle_has_sidecar') == 'on'

            car = Car(car_make, car_model, car_year, car_num_doors)
            motorcycle = Motorcycle(motorcycle_make, motorcycle_model, motorcycle_year, motorcycle_has_sidecar)
            
            return render_template('vehicle.html', car=car, motorcycle=motorcycle)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return render_template('error.html', error_message="An error occurred. Please try again later."), 500
    else:
        return render_template('index.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message="An internal server error occurred. Please try again later."), 500

if __name__ == '__main__':
    app.run(debug=True)
