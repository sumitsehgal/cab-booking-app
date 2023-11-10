# Adding this for local run, in prod environmet it will be setup using path
import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)

from common_utils.utils import Singleton, Database
from boundary import BoundaryHelper
import requests
from bson.son import SON

class LiveLocation(Singleton):

    def __init__( self ):
        super().__init__()
        self.collection_name = 'live_location'
        self.boundaryHelper = BoundaryHelper(13.0798, 80.2846, 20.0)
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
        nearest_query = {'location': SON([("$near", {'type' :'Point','coordinates' :[latitude, longitude]}), ("$maxDistance", 1000)])}
        all_records = Database.get_instance().get_multiple_data(self.collection_name, nearest_query)
        return all_records


def main():
    # Checkling SingleTon for each
    print(LiveLocation.get_instance().boundaryHelper._service_area)

if __name__ == "__main__":
    main()