import json
import requests

BASE_HTTP_URL = "http://localhost:8090/api/v1/"

def get_all_cabs():
    req_url = BASE_HTTP_URL + "booking/cabs"
    response = requests.post(req_url, json = { 'user_id' : 'Sumit-7988929968','user_location' :[12.931075969682226, 80.4564266751934]})
    return response.json()['taxis_location']

def confirm_booking(booking_id):
    req_url = BASE_HTTP_URL + "booking/confirm"
    response = requests.post(req_url, json = {'booking_id': booking_id})
    print(response)

def cancel_booking(booking_id):
    req_url = BASE_HTTP_URL + "booking/cancel"
    response = requests.post(req_url, json = {'booking_id': booking_id})
    print(response)

def main():
    taxis = get_all_cabs()
    print(taxis)
    #confirm_booking(booking_id)
    #cancel_booking(booking_id)
    #confirm_booking('Sumit-7988929968-11:40:34')
    #cancel_booking("Fahad-9820775814-17:44:23")

if __name__ == "__main__":
    main()