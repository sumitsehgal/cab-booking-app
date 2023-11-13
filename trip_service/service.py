from flask import Flask, jsonify, request, Blueprint
from trip import TripModel, TripStatus

app = Flask("Trip-Service")

# Versioning API
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# To start a trip
@api_v1.route("/trip/start", methods=["POST"])
def start_trip():
    request_data = request.get_json()
    trip_result = TripModel.get_instance().start_trip(**request_data)
    
    if trip_result['status'] == TripStatus.InProgress:
        return jsonify(trip_result)
    else:
        return jsonify({'error': 'Failed to start trip'}), 400

# To complete a trip
@api_v1.route("/trip/complete", methods=["POST"])
def complete_trip():
    request_data = request.get_json()
    trip_id = request_data.get('trip_id')
    amount = request_data.get('amount')  # Assuming you want to process payment on completion
    trip_result = TripModel.get_instance().complete_trip(trip_id, amount)
    
    if trip_result['status'] == TripStatus.Completed:
        # Process payment
        # payment_result = PaymentService.get_instance().process_payment(trip_id, amount)
        payment_result = True
        return jsonify({'trip_status': trip_result, 'payment_status': payment_result})
    else:
        return jsonify({'error': 'Failed to complete trip'}), 400

# To cancel a trip
@api_v1.route("/trip/cancel", methods=['POST'])
def cancel_trip():
    request_data = request.get_json()
    trip_id = request_data.get('trip_id')
    trip_result = TripModel.get_instance().cancel_trip(trip_id)
    
    if trip_result['status'] == TripStatus.Cancelled:
        return jsonify(trip_result)
    else:
        return jsonify({'error': 'Failed to cancel trip'}), 400

# Registering Blueprint
app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8095)
