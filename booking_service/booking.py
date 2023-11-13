# Adding this for local run, in prod environmet it will be setup using path
import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)

from common_utils.utils import Singleton, Database
from bson.son import SON
import requests
import datetime
import time
from enum import StrEnum
import logging
logging.getLogger().setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

class BookingStatus(StrEnum):
    New = "New" # Booking not confirmed by user but found cabs near to his liocation
    User_Confirmed = "User_Confirmed" # Confirmed by user, 
    Confirm = "Confirm" # User has confirm the booking and cab is also alloted
    Cancelled = "Cancelled" # User cancel the booking before trip is started
    No_Cabs = "No-Cabs"


class RequestConstant(StrEnum):
    User_Location = 'user_location'
    Destination = 'destination'
    User_Id = 'user_id'
    Booking_Id = "booking_id"

class LiveLocationConstants(StrEnum):
    Latitude = 'latitude'
    Longitude = 'longitude'


class BookingModel(Singleton):

    def __init__(self):
        super().__init__()
        self.collection_name = 'bookings'
        self.live_location_url = "http://localhost:8085/api/v1/find/taxi"


    def _get_new_booking_document( self, user_id, user_location, destination,taxis ):
        booking_data = { 
            'booking_id' : "{0}-{1}".format(user_id, datetime.datetime.now().strftime("%H:%M:%S")),
            'user_id' : user_id,
            'user_location' : { 'type' : 'Point', 'coordinates' : [user_location[0], user_location[1]]},
            'destination' :{ 'type' : 'Point', 'coordinates' : [destination[0], destination[1]]},
            'status' : BookingStatus.New,
            'taxis' : taxis,
            'taxi_alloted' :[],
        }
        logging.info("Creating new booking request: {0}".format(booking_data['booking_id']))
        return booking_data

    def _get_status_update(self, status):
        return { 'status' : status }
    
    def _get_key( self, booking_id):
        return {'booking_id' : booking_id}
    
    def _query_location_service(self, user_location):
        logging.info(user_location)
        req_data = {LiveLocationConstants.Latitude: user_location[0], LiveLocationConstants.Longitude : user_location[1]}
        req_response = requests.post(self.live_location_url, json=req_data)
        # Need Response validation
        if req_response.status_code == 200:
            return req_response.json()
        else:
            logging.error("Failed to get nearby taxi: {}".format(req_response.status_code))
            return []
        
    def _send_notofication_to_driver(self, booking_key):
        pass


    def get_nearby_taxis(self, request_data):
        user_location = request_data.get(RequestConstant.User_Location)
        destination = request_data.get(RequestConstant.Destination)
        user_id = request_data.get(RequestConstant.User_Id)
        logging.info("{}-{}-{}".format(user_id,user_location,destination))
        documents = self._query_location_service(user_location)
        cabs = []
        cabs_location = []
        for document in documents:
            cabs.append(document.get('taxi_number'))
            cabs_location.append(document['location']['coordinates'])
        if cabs:
            logging.info("Found {0} cabs nearby for {1}".format(len(cabs), user_location))
            booking_data = self._get_new_booking_document(user_id=user_id, user_location=user_location, destination=destination,taxis=cabs)
            Database.get_instance().insert_single_data(self.collection_name, booking_data)
            return { 'booking_id' : booking_data['booking_id'], 'user_id' : user_id, 'taxis_location' : cabs_location, 'destination':destination}
        else:
            logging.warn("No cabs found")
            return {}

    def confirm_booking(self, request_data):
        booking_id = request_data.get(RequestConstant.Booking_Id)
        if booking_id:
            logging.info("Confirming booking for {0}".format(booking_id))
            update_data = self._get_status_update(BookingStatus.User_Confirmed)
            update_key = self._get_key(booking_id)
            Database.get_instance().update_single_data(self.collection_name, update_key, update_data)
            self._send_notofication_to_driver(update_key)
            time.sleep(180) # Wait for 3 minutes
            document = Database.get_instance().get_single_data(self.collection_name, {'booking_id' : booking_id})
            if document and document['status'] == BookingStatus.Confirm:
                return {'booking_id' : booking_id, 'status' : BookingStatus.Confirm, 'taxi' : document['taxi_alloted'] }
            else:
                # After 3 mins since no cab was found setting status to No_cabs
                update_data = self._get_status_update(BookingStatus.No_Cabs)
                Database.get_instance().update_single_data(self.collection_name, update_key, update_data)
                return {'booking_id' : booking_id, 'status' : BookingStatus.No_Cabs, 'taxi' : []}
        else:
            logging.warn("Booking request received without booking id.")
            return {}

    def cancel_booking(self, request_data):
        booking_id = request_data.get(RequestConstant.Booking_Id)
        if booking_id:
            update_data = self._get_status_update(BookingStatus.Cancelled)
            update_key = self._get_key(booking_id)
            Database.get_instance().update_single_data(self.collection_name, update_key, update_data)
            return { 'Status' : 'Booking Deleted'} 
        else:
            logging.warn("Cancel booking request received without booking id.")
            return { 'Status' : 'Booking Deleted'}
        
    def get_booking_by_id(self, request_data):
        booking_id = request_data.get(RequestConstant.Booking_Id)
        if booking_id is None:
            return {'Status': False, 'Message': 'Booking ID not Exists'}
        get_key = self._get_key(booking_id)
        booking = Database.get_instance().get_single_data(self.collection_name, get_key)
        if booking is None:
            return {'Status': False, 'Message': 'Booking not Exists'}
        
        return {
            'Status': True,
            'Data': booking
        }



