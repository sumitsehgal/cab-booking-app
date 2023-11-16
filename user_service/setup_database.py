"""
This module will do all setup required for Database.
It will create 
1. Database
2. It will create users collection
3. It will create drivers collection
4. It will create live_locations collection
"""
from pymongo import MongoClient
import logging
from users import Users, Taxis, Drivers

from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Logging Path
# Configure the logging system
log_file = os.getenv('LOG_FILE')
logging.basicConfig(filename=log_file, level=logging.INFO)



#import dns.resolver
#dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)


def get_database():
    db_client = MongoClient(f'mongodb://{DB_HOST}:{DB_PORT}')
    db_names = db_client.list_database_names()
    if DB_NAME in db_names:
        logging.info("Database already present, skipping creation of database")
    else:
        db_client[DB_NAME]
        logging.info("Database created")
    return db_client[DB_NAME]

def create_collections(database):
    # Remember till there is no data, collections are not created, so setting up some random data
    # Create users collection
    print("Creating users")
    database['users']
    Users.get_instance().add("Fahad", "Mustafa", "Madani", "9820775814", "Mumbai")
    # Create drivers collection
    database['drivers']
    Drivers.get_instance().add("Fahad-2", "Mustafa", "Madani", "9820775814", "Mumbai")
    # Creating taxi collection
    database['taxis']
    Taxis.get_instance().add("MH-02-AA-1234", "Luxury", "Mumbai", "Fahad-2",2018, 4, "Available", "Diesel" )

    
def main():
    database = get_database()
    create_collections(database)

def load_data()
    ## To read the users data file and add data to the users collection    
    with open('users_data.csv', 'r') as user_fh:
        for row in user_fh:
            row = row.rstrip()
            if row:
                (first_name, middle_name, last_name, email_id, mobile_number, city, emergency_no) = row.split(',')
                users=Users()
                users.add(first_name, middle_name, last_name, email_id, mobile_number, city, emergency_no)

    # Read drivers data file and insert into drivers collection
    with open('drivers_data.csv', 'r') as driver_fh:
        for row in driver_fh:
            row = row.rstrip()
            if row:
                (first_name, middle_name, last_name, email_id, mobile_number, city, emergency_no) = row.split(',')
                drivers=Drivers()
                drivers.add(first_name, middle_name, last_name, email_id, mobile_number, city, emergency_no)

    # Read taxi data file and insert into taxi collection

    with open('taxis_data.csv', 'r') as taxi_fh:
        for row in taxi_fh:
            row = row.rstrip()
            if row:
                (taxi_number,taxi_type,city,driver_name,Year_of_man,seating_capacity,avail_status,fuel_type) = row.split(',')
                taxi=Taxis()
                taxi.add(taxi_number,taxi_type,city,driver_name,Year_of_man,seating_capacity,avail_status,fuel_type)
    

if __name__ == "__main__":
    main()
    load_data()
