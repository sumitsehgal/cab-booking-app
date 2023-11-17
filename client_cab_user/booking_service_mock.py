import json
import requests

BASE_HTTP_URL = "http://localhost:8090/api/v1/"

def get_all_cabs():
    req_url = BASE_HTTP_URL + "booking/cabs"
    response = requests.post(req_url, json = { 'user_id' : 'Sumit-7988929968','user_location' :[12.931075969682226, 80.4564266751934]})
    return response.json()['taxis_location']

def confirm_booking():
    req_url = BASE_HTTP_URL + "booking/confirm"
    response = requests.post(req_url, json = {'user_id' : 'Fahad-9820775814', 'user_location' : [12.931075969682226, 80.4564266751934], 'destination' : [12.899520179224464, 80.4531823786293]})
    print(response.status_code, response.json())

def cancel_booking(booking_id):
    req_url = BASE_HTTP_URL + "booking/cancel"
    response = requests.post(req_url, json = {'booking_id': booking_id})
    print(response)

def accept_booking():
    req_url = BASE_HTTP_URL + "/booking/accept"
    req_data = { 'booking_id' : 'First Name-65478-01-36-55', 'taxi_id': 'Taxi-11'}
    response = requests.post(req_url, json = req_data)
    print(response)

def check_for_booking():
    req_url = BASE_HTTP_URL + "/booking/check/trip"
    req_data = { 'taxi_id': 'Taxi-11'}
    response = requests.post(req_url, json = req_data)
    print(response.json())
    

def driver_booking_action_reject():
    req_url = BASE_HTTP_URL + 'booking/driver/action'
    req_data = { 'taxi_id' : 'Taxi-11', 'booking_id' : 'First Name-65478-17-40-29', 'status' : 'Reject'}
    response = requests.post(req_url, json = req_data)
    print(response.json())

def driver_booking_action_accept():
    req_url = BASE_HTTP_URL + 'booking/driver/action'
    req_data = { 'taxi_id' : 'Taxi-11', 'booking_id' : 'First Name-65478-17-40-28', 'status' : 'Accept'}
    response = requests.post(req_url, json = req_data)
    print(response.json())

def main():
    #taxis = get_all_cabs()
    #print(taxis)
    #confirm_booking()
    #cancel_booking(booking_id)
    #confirm_booking('Sumit-7988929968-11:40:34')
    #cancel_booking("Fahad-9820775814-17:44:23")
    #accept_booking()
    #check_for_booking()
    #driver_booking_action_reject()
    driver_booking_action_accept()
    pass

if __name__ == "__main__":
    main()