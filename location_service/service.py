from flask import Flask, jsonify, request, Blueprint
from setup_boundary import BoundaryService
from update_live_location import LiveLocationService

app = Flask("Location-Service")

# Versioning API
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api_v1.route("/boundary/<locparm>", methods=["GET"])
def get_boundary_points(locparm):
    boundarypt = BoundaryService().geodesic_point_buffer(locparm)
    return jsonify({'Status':"Ok", "Data": boundarypt})

@api_v1.route("/boundary/<boundarypt>", methods=["GET"])
def get_min_max_coordinates(boundarypt):
    minmaxcoordinate = BoundaryService().minmaxcoordinates(boundarypt)
    return jsonify({'Status':"Ok", "Data": minmaxcoordinate})

@api_v1.route("/taxi/<locparm>", methods=["PATCH"])
def update_loc(locparm):
    request_data = request.get_json()
    LiveLocationService.updliveloc(locparm)
    return jsonify({'Status':"Ok"})