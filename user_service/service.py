from flask import Flask, jsonify, request 

app = Flask("'User-Service")

@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify({'Cab User':user_id})


@app.route("/user", methods=["POST"])
def put_user():
    if request.method == 'POST':
        request_data = request.get_json()
    return jsonify({'Status':'Ok', 'Cab User' : request_data['Name']})


@app.route("/driver/<driver_id>")
def get_driver(driver_id):
    return jsonify({'Driver':driver_id})

@app.route("/driver", methods=["POST"])
def put_driver():
    if request.method == 'POST':
        request_data = request.get_json()
    return jsonify({'Status':'Ok', 'Cab User' : request_data['Name']})


if __name__ == "__main__":
    app.run(debug=True)