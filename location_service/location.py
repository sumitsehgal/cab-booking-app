from utils import Singleton, Database
from boundary import BoundaryHelper

class LiveLocation(Singleton):

    def __init__( self ):
        super().__init__()
        self.collection_name = 'live_location'
        self.boundaryHelper = BoundaryHelper(13.0798, 80.2846, 20.0)

    def __get_data_from_json(self, json_data):
        lat = json_data.get('latitude', None)
        lon = json_data.ge('longitude', None)
        taxi_id = json_data.get('taxi_id')

    def update_location(self, json_data ):
        lat = json_data.get('latitude', None)
        lon = json_data.get('longitude', None)
        taxi_id = json_data('taxi_id', None)
        if self.boundaryHelper.is_in_service_boundary(lat, lon) and taxi_id:
            key = { 'taxi_id' : taxi_id }
            loc_data = { 'latitude': lat, 'longitude' : lon }
            return Database.get_instance().update_single_data(self.collection_name, key, json_data)
    
    def get_count_key(self, key):
        count_key = Database.get_instance().count_documents(self.collection_name,key)
        return count_key
    
    def get_by_number( self, taxi_number):
        query = {'taxi_number': taxi_number}
        return Database.get_instance().get_single_data(self.collection_name, query)

def main():
    # Checkling SingleTon for each
    print(LiveLocation.get_instance())

if __name__ == "__main__":
    main()