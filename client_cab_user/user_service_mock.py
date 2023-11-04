from collections import namedtuple
import json
import requests

User = namedtuple( 'User', [ 'first_name', 'middle_name', 'last_name', 'mobile', 'city'])
CITY = "Mumbai"

UserList = [
    User("Fahad", "", "Madani", 9820775814, CITY),
    User("Sumit", "", "Sehgal", 7988929968, CITY),
    User("Prakash", "", "G", 9444022463, CITY),
    User("Sankar", "", "Balasubrahmanian", 9840033343, CITY),
    User("Shivani", "", "", 9350087493, CITY),
    User("Sunil", "", "Yadav", 8505940663, CITY),
    User("Harshita", "", "Agarwal", 9289372841, CITY),
    User("Fahad-1", "", "Madani-1", 9820775814, CITY),
    User("Sumit-1", "", "Sehgal-1", 7988929968, CITY),
    User("Prakash-1", "", "G-1", 9444022463, CITY),
]

BASE_HTTP_URL = "http://localhost:8080/api/v1/"

def get_user_json(user):
    data = {
        'first_name' : user.first_name,
        'middle_name' : user.middle_name,
        'last_name' : user.last_name,
        'mobile_number' : user.mobile,
        'city' : user.city
    }
    return data


def mock_user_creation():
    req_url = BASE_HTTP_URL + "user"
    for user in UserList:
        response = requests.post(req_url, json = get_user_json(user))
        print( response )
        print(response.json())


def mock_driver_creation():
    req_url = BASE_HTTP_URL + "driver"
    # Since the collection for driver is same, using the same
    for user in UserList:
        response = requests.post(req_url, json = get_user_json(user))
        print( response )
        print(response.json())


def main():
    #mock_user_creation()
    mock_driver_creation()

if __name__ == "__main__":
    main()