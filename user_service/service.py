from lib2to3.pgen2.driver import Driver
from flask import Flask, jsonify, request, Blueprint
from users import Users, Drivers, Taxis
import json

app = Flask("'User-Service")

# Versioning API
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_v1.route("/user", methods=["GET"])
def list_user():
    # page = int(request.args.get('page', 1))
    # limit = int(request.args.get('limit', 15))
    # users = Users().get_list_with_pagination(page=page, limit=limit)
    # users = json.dumps(users, default=str)
    users = Users().get_instance().get_all()
    return jsonify({'Status':"Ok", "Data": users})

@api_v1.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    user = Users().get_instance().get_by_id(user_id)
    return jsonify({'Status':"Ok", "Data": user})


@api_v1.route("/user", methods=["POST"])
def add_user():
    if request.method == 'POST':
        request_data = request.get_json()
        isUserAdded = Users.get_instance().add(request_data)
        
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
    drivers = Drivers().get_instance().get_all()
    return jsonify({'Status':"Ok", "Data": drivers})

@api_v1.route("/driver/<driver_id>", methods=["GET"])
def get_driver(driver_id):
    driver = Drivers().get_instance().get_by_id(driver_id)
    return jsonify({'Status':"Ok", "Data": driver})


@api_v1.route("/driver", methods=["POST"])
def add_driver():
    if request.method == 'POST':
        request_data = request.get_json()
        isDriverAdded = Drivers.get_instance().add(request_data)
        
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

@api_v1.route("/taxi", methods=["GET"])
def get_taxis():
    return jsonify(Taxis.get_instance().get_all())


@api_v1.route("/taxi", methods=["POST"])
def add_taxi():
    request_data = request.get_json()
    is_taxi_added = Taxis.get_instance().add(request_data)
    if is_taxi_added is None:
            return jsonify({'Status':'Error', 'Message': "Problem in adding Taxi"})
    return jsonify({'Status':'Ok'})


# Registering Blueprint
app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)