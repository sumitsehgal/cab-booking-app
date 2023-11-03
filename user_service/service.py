from flask import Flask, jsonify, request, Blueprint
from user_service.users import Drivers
from users import Users

app = Flask("'User-Service")

# Versioning API
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_v1.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    user = Users().get_by_id(user_id)
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


@api_v1.route("/driver/<driver_id>")
def get_driver(driver_id):
    driver = Drivers.get_instance().get_by_id(driver_id)
    return jsonify({'Status':"Ok", "Data": driver})

@api_v1.route("/driver", methods=["POST"])
def put_driver():
    request_data = request.get_json()
    isUserAdded = Drivers.get_instance().add(request_data)
    if isUserAdded is None:
        return jsonify({'Status':'Error', 'Message': "There is problem while registering"})
    return jsonify({'Status':'Ok', 'UserId': str(isUserAdded), 'Name': request_data['first_name']})



# Registering Blueprint
app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)