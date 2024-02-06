from flask import Blueprint, jsonify, request
import json

RuffelBagAB = Blueprint("RuffelBagAB", __name__)


#Load data from JSON-file
try:
    with open('/cars.json', 'r') as file:
        cars = json.load(file)
except FileNotFoundError:
    cars = []


#Get all cars
@RuffelBagAB.route('/', methods=['GET'])
def get_cars_jsonlist():
    return jsonify({'cars': cars})


#Get a specific car by brand
@RuffelBagAB.route('/<brand>', methods=['GET'])
def get_car_jsonlist(brand):
    for car in cars:
        if car['brand'] == brand:
            return jsonify({'brand': car})

    return jsonify({'error': 'Car not found!'}), 404 # 404 Not Found, resource can't be found


# Delete a car by plate number
@RuffelBagAB.route('/<plate>', methods=['DELETE'])
def delete_car(plate):
    # Find the car by plate number and remove it
    for car in cars:
        if car['platenumber'] == plate:
            cars.remove(car)
            with open('cars.json', 'w') as file:
                json.dump(cars, file, indent=2)
            return jsonify({'message': 'Car deleted successfully!'})

    return jsonify({'error': 'Car not found!'}), 404 # 404 Not Found, resource can't be found


# Update a car by plate number
@RuffelBagAB.route('/<plate>', methods=['PUT'])
def update_car(plate):
    brand = request.json['brand']

    # Find the car by plate number and update
    for car in cars:
        if car['platenumber'] == plate:
            car['brand'] = brand
            with open('cars.json', 'w') as file:
                json.dump(cars, file, indent=2)
            return jsonify({'message': 'Car updated successfully!'})

    return jsonify({'error': 'Car not found!'}), 404 # 404 Not Found, resource can't be found


#Create a new car
@RuffelBagAB.route('/', methods=['POST'])
def add_car():
    brand = request.json['brand']
    platenumber = request.json['platenumber']

    #Check if car already exists
    for car in cars:
        if car['platenumber'] == platenumber:
            return jsonify({'error': 'Car already exists!'}), 400 # 400 Bad Request

    new_car = {'brand': brand, 'platenumber': platenumber}
    cars.append(new_car)

    with open('cars.json', 'w') as file:
        json.dump(cars, file,indent=2)

    return jsonify({'message': 'Car added successfully!'}), 201 # 201 created


if __name__ == '__main__':
    RuffelBagAB.run(debug=True)
