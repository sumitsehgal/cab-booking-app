from collections import namedtuple
import json
import requests

User = namedtuple( 'User', [ 'first_name', 'middle_name', 'last_name', 'email', 'mobile', 'city'])
Taxi = namedtuple("Taxi", ['taxi_number', 'taxi_type', 'city', 'driver'])

CITY = "Mumbai"

UserList = [
    User("Fahad", "", "Madani", "fsmadani@gmail.com", 9820775814, CITY),
    User("Sumit", "", "Sehgal", "theprofessional1992@gmail.com", 7988929968, CITY),
    User("Prakash", "", "G", "prakkig@gmail.com", 9444022463, CITY),
    User("Sankar", "", "Balasubrahmanian", "bsankar99@gmail.com", 9840033343, CITY),
    User("Shivani", "", "", "shivani11aggarwal@yahoo.co.in",  9350087493, CITY),
    User("Sunil", "", "Yadav", "skyadavcs2020@gmail.com", 8505940663, CITY),
    User("Harshita", "", "Agarwal", "harshita.agarwal@greatlearning.in", 9289372841, CITY),
    User("Fahad-1", "", "Madani-1", "fsmadani+1@gmail.com", 9820775814, CITY),
    User("Sumit-1", "", "Sehgal-1", "theprofessional1992+1@gmail.com", 7988929968, CITY),
    User("Prakash-1", "", "G-1", "prakkig+1@gmail.com", 9444022463, CITY),
]

BASE_HTTP_URL = "http://localhost:8080/api/v1/"

def get_user_json(user):
    data = {
        'first_name' : user.first_name,
        'middle_name' : user.middle_name,
        'last_name' : user.last_name,
        'email': user.email,
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


DriverList = [
    User('Driver-11', '', '', 'driver-1@gmail.com', 1, 'CITY'),
    User('Driver-12', '', '', 'driver-2@gmail.com', 2, 'CITY'),
    User('Driver-13', '', '', 'driver-3@gmail.com', 3, 'CITY'),
    User('Driver-14', '', '', 'driver-4@gmail.com', 4, 'CITY'),
    User('Driver-15', '', '', 'driver-5@gmail.com', 5, 'CITY'),
    User('Driver-16', '', '', 'driver-6@gmail.com', 6, 'CITY'),
    User('Driver-17', '', '', 'driver-7@gmail.com', 7, 'CITY'),
    User('Driver-18', '', '', 'driver-8@gmail.com', 8, 'CITY'),
    User('Driver-19', '', '', 'driver-9@gmail.com', 9, 'CITY'),
    User('Driver-110', '', '', 'driver-10@gmail.com', 10, 'CITY'),
    User('Driver-111', '', '', 'driver-11@gmail.com', 11, 'CITY'),
    User('Driver-112', '', '', 'driver-12@gmail.com', 12, 'CITY'),
    User('Driver-113', '', '', 'driver-13@gmail.com', 13, 'CITY'),
    User('Driver-114', '', '', 'driver-14@gmail.com', 14, 'CITY'),
    User('Driver-115', '', '', 'driver-15@gmail.com', 15, 'CITY'),
    User('Driver-116', '', '', 'driver-16@gmail.com', 16, 'CITY'),
    User('Driver-117', '', '', 'driver-17@gmail.com', 17, 'CITY'),
    User('Driver-118', '', '', 'driver-18@gmail.com', 18, 'CITY'),
    User('Driver-119', '', '', 'driver-19@gmail.com', 19, 'CITY'),
    User('Driver-120', '', '', 'driver-20@gmail.com', 20, 'CITY'),
    User('Driver-121', '', '', 'driver-21@gmail.com', 21, 'CITY'),
    User('Driver-122', '', '', 'driver-22@gmail.com', 22, 'CITY'),
    User('Driver-123', '', '', 'driver-23@gmail.com', 23, 'CITY'),
    User('Driver-124', '', '', 'driver-24@gmail.com', 24, 'CITY'),
    User('Driver-125', '', '', 'driver-25@gmail.com', 25, 'CITY'),
    User('Driver-126', '', '', 'driver-26@gmail.com', 26, 'CITY'),
    User('Driver-127', '', '', 'driver-27@gmail.com', 27, 'CITY'),
    User('Driver-128', '', '', 'driver-28@gmail.com', 28, 'CITY'),
    User('Driver-129', '', '', 'driver-29@gmail.com', 29, 'CITY'),
    User('Driver-130', '', '', 'driver-30@gmail.com', 30, 'CITY'),
    User('Driver-131', '', '', 'driver-31@gmail.com', 31, 'CITY'),
    User('Driver-132', '', '', 'driver-32@gmail.com', 32, 'CITY'),
    User('Driver-133', '', '', 'driver-33@gmail.com', 33, 'CITY'),
    User('Driver-134', '', '', 'driver-34@gmail.com', 34, 'CITY'),
    User('Driver-135', '', '', 'driver-35@gmail.com', 35, 'CITY'),
    User('Driver-136', '', '', 'driver-36@gmail.com', 36, 'CITY'),
    User('Driver-137', '', '', 'driver-37@gmail.com', 37, 'CITY'),
    User('Driver-138', '', '', 'driver-38@gmail.com', 38, 'CITY'),
    User('Driver-139', '', '', 'driver-39@gmail.com', 39, 'CITY'),
    User('Driver-140', '', '', 'driver-40@gmail.com', 40, 'CITY'),
    User('Driver-141', '', '', 'driver-41@gmail.com', 41, 'CITY'),
    User('Driver-142', '', '', 'driver-42@gmail.com', 42, 'CITY'),
    User('Driver-143', '', '', 'driver-43@gmail.com', 43, 'CITY'),
    User('Driver-144', '', '', 'driver-44@gmail.com', 44, 'CITY'),
    User('Driver-145', '', '', 'driver-45@gmail.com', 45, 'CITY'),
    User('Driver-146', '', '', 'driver-46@gmail.com', 46, 'CITY'),
    User('Driver-147', '', '', 'driver-47@gmail.com', 47, 'CITY'),
    User('Driver-148', '', '', 'driver-48@gmail.com', 48, 'CITY'),
    User('Driver-149', '', '', 'driver-49@gmail.com', 49, 'CITY'),
    User('Driver-150', '', '', 'driver-50@gmail.com', 50, 'CITY')
]


def mock_driver_creation():
    req_url = BASE_HTTP_URL + "driver"
    # Since the collection for driver is same, using the same
    for user in DriverList:
        print("user", get_user_json(user))
        response = requests.post(req_url, json = get_user_json(user))
        print( response )
        print(response.json())


TaxiList = [
    Taxi('Taxi-11', 'Mini', CITY, 'Driver-11'),
    Taxi('Taxi-12', 'Sedan', CITY, 'Driver-12'),
    Taxi('Taxi-13', 'Luxury', CITY, 'Driver-13'),
    Taxi('Taxi-14', 'Mini', CITY, 'Driver-14'),
    Taxi('Taxi-15', 'Sedan', CITY, 'Driver-15'),
    Taxi('Taxi-16', 'Luxury', CITY, 'Driver-16'),
    Taxi('Taxi-17', 'Mini', CITY, 'Driver-17'),
    Taxi('Taxi-18', 'Sedan', CITY, 'Driver-18'),
    Taxi('Taxi-19', 'Luxury', CITY, 'Driver-19'),
    Taxi('Taxi-110', 'Mini', CITY, 'Driver-110'),
    Taxi('Taxi-111', 'Sedan', CITY, 'Driver-111'),
    Taxi('Taxi-112', 'Luxury', CITY, 'Driver-112'),
    Taxi('Taxi-113', 'Mini', CITY, 'Driver-113'),
    Taxi('Taxi-114', 'Sedan', CITY, 'Driver-114'),
    Taxi('Taxi-115', 'Luxury', CITY, 'Driver-115'),
    Taxi('Taxi-116', 'Mini', CITY, 'Driver-116'),
    Taxi('Taxi-117', 'Sedan', CITY, 'Driver-117'),
    Taxi('Taxi-118', 'Luxury', CITY, 'Driver-118'),
    Taxi('Taxi-119', 'Mini', CITY, 'Driver-119'),
    Taxi('Taxi-120', 'Sedan', CITY, 'Driver-120'),
    Taxi('Taxi-121', 'Luxury', CITY, 'Driver-121'),
    Taxi('Taxi-122', 'Mini', CITY, 'Driver-122'),
    Taxi('Taxi-123', 'Sedan', CITY, 'Driver-123'),
    Taxi('Taxi-124', 'Luxury', CITY, 'Driver-124'),
    Taxi('Taxi-125', 'Mini', CITY, 'Driver-125'),
    Taxi('Taxi-126', 'Sedan', CITY, 'Driver-126'),
    Taxi('Taxi-127', 'Luxury', CITY, 'Driver-127'),
    Taxi('Taxi-128', 'Mini', CITY, 'Driver-128'),
    Taxi('Taxi-129', 'Sedan', CITY, 'Driver-129'),
    Taxi('Taxi-130', 'Luxury', CITY, 'Driver-130'),
    Taxi('Taxi-131', 'Mini', CITY, 'Driver-131'),
    Taxi('Taxi-132', 'Sedan', CITY, 'Driver-132'),
    Taxi('Taxi-133', 'Luxury', CITY, 'Driver-133'),
    Taxi('Taxi-134', 'Mini', CITY, 'Driver-134'),
    Taxi('Taxi-135', 'Sedan', CITY, 'Driver-135'),
    Taxi('Taxi-136', 'Luxury', CITY, 'Driver-136'),
    Taxi('Taxi-137', 'Mini', CITY, 'Driver-137'),
    Taxi('Taxi-138', 'Sedan', CITY, 'Driver-138'),
    Taxi('Taxi-139', 'Luxury', CITY, 'Driver-139'),
    Taxi('Taxi-140', 'Mini', CITY, 'Driver-140'),
    Taxi('Taxi-141', 'Sedan', CITY, 'Driver-141'),
    Taxi('Taxi-142', 'Luxury', CITY, 'Driver-142'),
    Taxi('Taxi-143', 'Mini', CITY, 'Driver-143'),
    Taxi('Taxi-144', 'Sedan', CITY, 'Driver-144'),
    Taxi('Taxi-145', 'Luxury', CITY, 'Driver-145'),
    Taxi('Taxi-146', 'Mini', CITY, 'Driver-146'),
    Taxi('Taxi-147', 'Sedan', CITY, 'Driver-147'),
    Taxi('Taxi-148', 'Luxury', CITY, 'Driver-148'),
    Taxi('Taxi-149', 'Mini', CITY, 'Driver-149'),
    Taxi('Taxi-150', 'Sedan', CITY, 'Driver-150')
]

def get_taxi_json(taxi_data):
    taxi_json = {
        'taxi_number' : taxi_data.taxi_number,
        'taxi_type' : taxi_data.taxi_type,
        'city' : taxi_data.city,
        'driver_id' : taxi_data.driver
    }
    return taxi_json

def mock_taxi_creation():
    req_url = BASE_HTTP_URL + "taxi"
    # Since the collection for driver is same, using the same
    for taxi  in TaxiList:
        response = requests.post(req_url, json = get_taxi_json(taxi))
        print( response )
        print(response.json())

def main():
    mock_user_creation()
    mock_driver_creation()
    mock_taxi_creation()
    pass
        
if __name__ == "__main__":
    main()