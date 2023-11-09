from lib2to3.pgen2.driver import Driver
from flask import Flask, jsonify, request, Blueprint
from users import Taxis, Users, Drivers
from json_encoder import CustomJSONEncoder 
import json

app = Flask("'User-Service")


# Versioning API
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# List of Users
@api_v1.route("/user", methods=["GET"])
def list_user():
    userLists = list(Users().get_instance().get_all())
    response_data = {'Status':"Ok", "Data": userLists}

    return jsonify(response_data)

@api_v1.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    user = Users().get_instance().get_by_id(user_id)
    return jsonify({'Status':"Ok", "Data": user})


@api_v1.route("/user", methods=["POST"])
def add_user():
    if request.method == 'POST':
        request_data = request.get_json()
        print(request_data)
        isUserAdded = Users.get_instance().add(
            first_name=request_data.get('first_name'),
            last_name=request_data.get('last_name'),
            middle_name=request_data.get('middle_name'),
            mobile_number=request_data.get('mobile_number'),
            city=request_data.get('city'),
            emergency_contact=request_data.get('emergency_contact'),
        )
        
        if isUserAdded is None:
            return jsonify({'Status':'Error', 'Message': "There is problem while registering"})
    return jsonify({'Status':'Ok', 'UserId': str(isUserAdded), 'Name': request_data['first_name']})


@api_v1.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    Users.get_instance().delete_by_id(user_id)
    return jsonify({'Status':"Ok"})

@api_v1.route("/user/<user_id>", methods=["PATCH"])
def update_user(user_id):
    request_data = request.get_json()
    Users.get_instance().edit(user_id, request_data)
    return jsonify({'Status':"Ok"})


@api_v1.route("/driver", methods=["GET"])
def list_driver():
    drivers = list(Drivers().get_instance().get_all())
    return jsonify({'Status':"Ok", "Data": drivers})

@api_v1.route("/driver/<driver_id>", methods=["GET"])
def get_driver(driver_id):
    driver = Drivers().get_instance().get_by_id(driver_id)
    return jsonify({'Status':"Ok", "Data": driver})


@api_v1.route("/driver", methods=["POST"])
def add_driver():
    if request.method == 'POST':
        request_data = request.get_json()
        isDriverAdded = Drivers.get_instance().add(
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
            middle_name=request_data['middle_name'],
            mobile_number=request_data['mobile_number'],
            city=request_data['city'],
            emergency_contact=request_data['emergency_contact'],
        )
        
        if isDriverAdded is None:
            return jsonify({'Status':'Error', 'Message': "There is problem while registering"})
    return jsonify({'Status':'Ok', 'DriverId': str(isDriverAdded), 'Name': request_data['first_name']})


@api_v1.route("/driver/<driver_id>", methods=["DELETE"])
def delete_driver(driver_id):
    Drivers.get_instance().delete_by_id(driver_id)
    return jsonify({'Status':"Ok"})

@api_v1.route("/driver/<driver_id>", methods=["PATCH"])
def update_driver(driver_id):
    request_data = request.get_json()
    Drivers.get_instance().edit(driver_id, request_data)
    return jsonify({'Status':"Ok"})


@api_v1.route("/taxi/<taxi_id>", methods=["GET"])
def get_taxi(taxi_id):
    taxi = Taxis().get_instance().get_by_id(taxi_id)
    return jsonify({'Status':"Ok", "Data": taxi})

@api_v1.route("/taxi", methods=["POST"])
def add_taxi():
    if request.method == 'POST':
        request_data = request.get_json()
        isTaxiAdded = Taxis.get_instance().add(
            taxi_number=request_data.get('taxi_number'),
            taxi_type=request_data.get('taxi_type'),
            city=request_data.get('city'),
            driver=request_data.get('driver'),
            year_of_manufacturing=request_data.get('year_of_manufacturing'),
            seating_capacity=request_data.get('seating_capacity'),
            availability_status=request_data.get('availability_status'),
            fuel_type=request_data.get('fuel_type'),
        )
        
        if isTaxiAdded is None:
            return jsonify({'Status':'Error', 'Message': "There is problem while registering"})
    return jsonify({'Status':'Ok', 'TaxiId': str(isTaxiAdded), 'taxi_number': request_data['taxi_number']})

@api_v1.route("/taxi/<taxi_id>", methods=["PATCH"])
def update_taxi(taxi_id):
    request_data = request.get_json()
    Taxis.get_instance().edit(taxi_id, request_data)
    return jsonify({'Status': "Ok"})


@api_v1.route("/taxi/<taxi_id>", methods=["DELETE"])
def delete_taxi(taxi_id):
    Taxis.get_instance().delete_by_id(taxi_id=taxi_id)
    return jsonify({'Status':"Ok"})

@api_v1.route("/taxi", methods=["GET"])
def list_taxi():
    taxis = list(Taxis().get_instance().get_all())
    return jsonify({'Status':"Ok", "Data": taxis})


# Registering Blueprint
app.register_blueprint(api_v1)

# Set JSON Encoder
app.json_encoder = CustomJSONEncoder

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)