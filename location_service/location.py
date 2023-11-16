# Adding this for local run, in prod environmet it will be setup using path
import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)

from common_utils.utils import Singleton, Database
from boundary import BoundaryHelper
import requests
from bson.son import SON
import logging

class LiveLocation(Singleton):

    def __init__( self ):
        super().__init__()
        self.collection_name = 'live_location'
        self.boundaryHelper = BoundaryHelper(21.1458, 79.0882, 20.0)
        self.get_all_taxis()
        self.index_created = False # Index creation is indempotent operation, so calling it multiple times is no-op, but for safety will call it once the first insert happen


    def get_all_taxis(self):
        req_url = 'http://localhost:8080/api/v1/taxi'
        req_response = requests.get(req_url,timeout=120)
        all_taxis = req_response.json()
        self.taxi_cache = { doc['taxi_number']: doc for doc in all_taxis['Data'] }


    def update_location(self, json_data ):
        lat = json_data.get('latitude', None)
        lon = json_data.get('longitude', None)
        taxi_number = json_data.get('taxi_number', None)
        # TODO: how to check boundary condition here
        if taxi_number in self.taxi_cache:
            key = { 'taxi_number' : taxi_number }
            update_data = { 'location': { 'type': "Point", 'coordinates': [lat, lon] }, 'taxi_number' : taxi_number }
            status = Database.get_instance().replace_one(self.collection_name, key, update_data)
            if not self.index_created:
                Database.get_instance().create_geo_index(self.collection_name, 'location' )

    
    def get_count_key(self, key):
        count_key = Database.get_instance().count_documents(self.collection_name,key)
        return count_key
    
    def get_by_number( self, taxi_number):
        query = {'taxi_number': taxi_number}
        document =  Database.get_instance().get_single_data(self.collection_name, query)
        return { 'taxi_number' : taxi_number, 'latitude' : document['location']['coordinates'][0], 'longitude' : document['location']['coordinates'][1]}
    
    def get_boundary_coordinates(self):
        return self.boundaryHelper.min_max_coordinates()
    
    def get_nearby_taxis(self,request_data):
        latitude = request_data.get('latitude')
        longitude = request_data.get('longitude')
        # Query to get all the cabs in 2 km range
        nearest_query = {'location': SON([("$near", {'type' :'Point','coordinates' :[latitude, longitude]}), ("$maxDistance", 2000)]), 'booked' : {"$not": {"$eq":True}}}
        all_records = Database.get_instance().get_multiple_data(self.collection_name, nearest_query)
        return all_records

    def mark_taxi_as_booked(self, request_data):
        taxi_number = request_data.get("taxi_number")
        if taxi_number:
            update_data = { 'booked' : True }
            update_key = { 'taxi_number' : taxi_number}
            updated_result = Database.get_instance().update_single_data(self.collection_name, update_key, update_data )
            logging.info("Updated : {} with id:{}".format(updated_result.modified_count, updated_result.upserted_id))
            return { "message" : "Taxi {0} is booked".format(taxi_number)}

    def mark_taxi_as_free(self, request_data):
        taxi_number = request_data.get("taxi_number")
        if taxi_number:
            update_data = { 'booked' : False }
            update_key = { 'taxi_number' : taxi_number}
            updated_result = Database.get_instance().update_single_data(self.collection_name, update_key, update_data )
            logging.info("Updated : {} with id:{}".format(updated_result.modified_count, updated_result.upserted_id))
            return { "message" : "Taxi {0} is free".format(taxi_number)}


def main():
    # Updating live location of Cabs
    Livelocation.update_location({'latitude':21.0117, 'longitude': 79.0122, 'taxi_number': 'MH11C1234'})
    Livelocation.update_location({'latitude':21.0229, 'longitude': 79.0119, 'taxi_number': 'MH11F1234'})
    Livelocation.update_location({'latitude':21.03, 'longitude': 79.02, 'taxi_number': 'MH11G1234'})
    Livelocation.update_location({'latitude':21.0129, 'longitude': 79.0672, 'taxi_number': 'MH11K1234'})
    Livelocation.update_location({'latitude':21.141, 'longitude': 79.1101, 'taxi_number': 'MH11A1234'})
    Livelocation.update_location({'latitude':21.145, 'longitude': 79.115, 'taxi_number': 'MH11L1234'})
    Livelocation.update_location({'latitude':21.1501, 'longitude': 79.1125, 'taxi_number': 'MH11S1234'})
    Livelocation.update_location({'latitude':21.175, 'longitude': 79.125, 'taxi_number': 'MH11W1234'})
    Livelocation.update_location({'latitude':21.1411, 'longitude': 79.09, 'taxi_number': 'MH11E1234'})
    Livelocation.update_location({'latitude':21.1451, 'longitude': 79.0815, 'taxi_number': 'MH11P1234'})
    Livelocation.update_location({'latitude':21.1403, 'longitude': 79.0589, 'taxi_number': 'MH11V1234'})
    Livelocation.update_location({'latitude':21.15, 'longitude': 79.15, 'taxi_number': 'MH11Z1234'})

    # Checkling SingleTon for each
    print(LiveLocation.get_instance().get_nearby_taxis({'latitude':21.0217, 'longitude': 79.0112}))
    print(LiveLocation.get_instance().mark_taxi_as_booked({'taxi_number' : 'MH11F1234'}))
    print(LiveLocation.get_instance().get_nearby_taxis({'latitude':21.1432, 'longitude': 79.1121}))
    print(LiveLocation.get_instance().mark_taxi_as_booked({'taxi_number' : 'MH11A1234'}))
    print(LiveLocation.get_instance().mark_taxi_as_free({'taxi_number' : 'MH11F1234'}))
    print(LiveLocation.get_instance().get_nearby_taxis({'latitude':21.1435, 'longitude': 79.0764}))
    print(LiveLocation.get_instance().mark_taxi_as_booked({'taxi_number' : 'MH11P1234'}))
    
if __name__ == "__main__":
    main()
