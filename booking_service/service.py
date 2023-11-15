from flask import Flask, jsonify, request, Blueprint
from booking import BookingModel


app = Flask("Location-Service")

# Versioning API
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# To get all the cabs for given Lattitude and longitude
@api_v1.route("/booking/cabs", methods=["POST"])
def cabs():
    request_data = request.get_json()
    print(request_data)
    return jsonify( BookingModel.get_instance().get_nearby_taxis(request_data) )
    

# To confirm the booking
@api_v1.route("/booking/confirm", methods=["POST"])
def confirm():
    request_data = request.get_json()
    return jsonify(BookingModel.get_instance().confirm_booking(request_data))

    
# To cancel the booking
@api_v1.route("/booking/cancel", methods=['POST'])
def cancel():
    request_data = request.get_json()
    return jsonify(BookingModel.get_instance().cancel_booking(request_data))

@api_v1.route(f"/booking/<booking_id>", methods=['GET'])
def get_booking(booking_id):
    return jsonify(BookingModel.get_instance().get_booking_by_id({'booking_id': booking_id}))

# sending notification to cabs 
@api_v1.route(f"/booking/chkmsg", methods=['GET'])
def chkmsg(cab_id):
    return jsonify(BookingModel.get_instance().checkmsg())

# Registering Blueprint
app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8090)