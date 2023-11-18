"""
This module will do all setup required for Database.
It will create 
1. Database
2. It will create users collection
3. It will create drivers collection
4. It will create live_locations collection
"""

import requests
BASE_HTTP_URL = "http://localhost:8080/api/v1/"

    
def main():
    add_users()
    add_drivers()
    add_taxis()
    

def add_users():
    print("*********** Adding Users ***********")
    with open('users_data.csv', 'r') as user_fh:
        for row in user_fh:
            row = row.rstrip()
            if row:
                (first_name, middle_name, last_name, email_id, mobile_number, city, emergency_no) = row.split(',')
                user_data = {
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "last_name": last_name,
                    "email": email_id,
                    "city": city,
                    "mobile_number": mobile_number,
                    "emergency_contact" : emergency_no
                }
                req_url = BASE_HTTP_URL + "user"
                response = requests.post(req_url, json = user_data)
                print("Status: {0} with Message: {1}".format(response.status_code, response.json()['message']))


def add_drivers():
    # Read drivers data file and insert into drivers collection
    print("*********** Adding Drivers ***********")
    with open('drivers_data.csv', 'r') as driver_fh:
        for row in driver_fh:
            row = row.rstrip()
            if row:
                (first_name, middle_name, last_name, email_id, mobile_number, city, emergency_no) = row.split(',')
                driver_data = {
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "last_name": last_name,
                    "email": email_id,
                    "city": city,
                    "mobile_number": mobile_number,
                    "emergency_contact" : emergency_no
                }
                req_url = BASE_HTTP_URL + "driver"
                response = requests.post(req_url, json = driver_data)
                print("Status: {0} with Message: {1}".format(response.status_code, response.json()['message']))


def add_taxis():
    print("*********** Adding Taxis ***********")
    with open('taxis_data.csv', 'r') as taxi_fh:
        for row in taxi_fh:
            row = row.rstrip()
            if row:
                (taxi_number,taxi_type,city,driver_name,Year_of_man,seating_capacity,avail_status,fuel_type) = row.split(',')
                taxi_data = {
                            'taxi_number' : taxi_number, # this should be unique
                            'taxi_type' : taxi_type,
                            'city' : city,
                            'driver' : driver_name if driver_name else '',
                            'year_of_manufacturing': Year_of_man,
                            'seating_capacity': seating_capacity,
                            'availability_status': avail_status,
                            'fuel_type': fuel_type,
                        }
                req_url = BASE_HTTP_URL + "taxi"
                response = requests.post(req_url, json = taxi_data)
                print("Status: {0} with Message: {1}".format(response.status_code, response.json()['message']))

if __name__ == "__main__":
    main()
