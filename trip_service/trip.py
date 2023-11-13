# Adding this for local run, in prod environmet it will be setup using path
import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)

from common_utils.utils import Singleton, Database
import datetime
from enum import StrEnum
import logging

logging.getLogger().setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

class TripStatus(StrEnum):
    InProgress = "In Progress"
    Completed = "Completed"
    Cancelled = "Cancelled"

class TripModel(Singleton):

    def __init__(self):
        super().__init__()
        self.collection_name = 'trips'

    def _get_new_trip_document(self, booking_id, taxi_alloted, user_location, destination):
        return {
            'trip_id': "{0}-{1}".format(booking_id, datetime.datetime.now().strftime("%H:%M:%S")),
            'booking_id': booking_id,
            'taxi_alloted': taxi_alloted,
            'status': TripStatus.InProgress,
            'user_location': {'latitude': user_location[0], 'longitude': user_location[1]}, # This is for getting precise location
            'destination': {'latitude': destination[0], 'longitude': destination[1]}, # This is for precise drop location to recalcuate the fare.
            'start_time': datetime.datetime.now(),
            'end_time': None,
        }

    def start_trip(self, booking_id, taxi_alloted):
        trip_data = self._get_new_trip_document(booking_id, taxi_alloted)
        Database.get_instance().insert_single_data(self.collection_name, trip_data)
        return {'trip_id': trip_data['trip_id'], 'status': trip_data['status']}

    def complete_trip(self, trip_id):
        update_data = {'status': TripStatus.Completed, 'end_time': datetime.datetime.now()}
        update_key = {'trip_id': trip_id}
        Database.get_instance().update_single_data(self.collection_name, update_key, update_data)
        # Need to Call Payment Service
        return {'trip_id': trip_id, 'status': TripStatus.Completed}

    def cancel_trip(self, trip_id):
        update_data = {'status': TripStatus.Cancelled, 'end_time': datetime.datetime.now()}
        update_key = {'trip_id': trip_id}
        Database.get_instance().update_single_data(self.collection_name, update_key, update_data)
        return {'trip_id': trip_id, 'status': TripStatus.Cancelled}