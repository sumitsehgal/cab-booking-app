from flask import Flask, jsonify, request, Blueprint
from location import LiveLocation

app = Flask("Location-Service")

# Versioning API
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api_v1.route("/taxi/update", methods=["POST"])
def update_loc():
    """
    API to update live location of taxi
    """
    request_data = request.get_json()
    LiveLocation.get_instance().update_location(request_data)
    # TODO: Check what needs to be returned
    return jsonify({'Status':"Ok"})

@api_v1.route("/taxi/<taxi_number>", methods=['GET'])
def get_location(taxi_number):
    """
    API to get the location of current taxi provided
    """
    return jsonify(LiveLocation.get_instance().get_by_number(taxi_number))

# Added for demo purpose only
@api_v1.route("/boundary/cordinates", methods=['GET'])
def get_boundary_cordionates():
    """
    AOI to get the Boundary co-ordinates
    """
    return jsonify(LiveLocation.get_instance().get_boundary_coordinates())


@api_v1.route("/find/taxi", methods=["POST"])
def get_nearby_taxis():
    """
    API to get nearby taxis given user location i.e. lattitude and longitude
    """
    request_data = request.get_json()
    return jsonify(LiveLocation.get_instance().get_nearby_taxis(request_data))

@api_v1.route("/taxi/free", methods= ["POST"])
def mark_taxi_free():
    """
    API to mark Taxi as available, so that it can be returned in near by taxi query
    """
    request_data = request.get_json()
    return jsonify(LiveLocation.get_instance().mark_taxi_as_free(request_data))

@api_v1.route("/taxi/booked", methods=["POST"])
def mark_taxi_booked():
    """
    API to mark Taxi as booked, so that it can be avoided in near by taxi query
    """
    request_data = request.get_json()
    return jsonify(LiveLocation.get_instance().mark_taxi_as_booked(request_data))


# Registering Blueprint
app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8085)