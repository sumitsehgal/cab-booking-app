from flask import Flask, jsonify, request, Blueprint
from location import LiveLocation

app = Flask("Location-Service")

# Versioning API
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api_v1.route("/taxi/update", methods=["POST"])
def update_loc():
    request_data = request.get_json()
    LiveLocation.get_instance().update_location(request_data)
    # TODO: Check what needs to be returned
    return jsonify({'Status':"Ok"})

@api_v1.route("/taxi/<taxi_number>", methods=['GET'])
def get_location(taxi_number):
    return jsonify(LiveLocation.get_instance().get_by_number(taxi_number))

# Added for demo purpose only
@api_v1.route("/boundary/cordinates", methods=['GET'])
def get_boundary_cordionates():
    return jsonify(LiveLocation.get_instance().get_boundary_coordinates())


@api_v1.route("/find/taxi", methods=["POST"])
def get_nearby_taxis():
    request_data = request.get_json()
    return jsonify(LiveLocation.get_instance().get_nearby_taxis(request_data))


# Registering Blueprint
app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8085)