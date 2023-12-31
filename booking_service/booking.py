# Adding this for local run, in prod environmet it will be setup using path
import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.pardir)

from common_utils.utils import Singleton, Database
from bson.son import SON
from math import sin, cos, sqrt, atan2, radians
import requests
import datetime
import time
from enum import StrEnum
from collections import defaultdict

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
    Taxi_Prefer = "taxi_prefer"

class LiveLocationConstants(StrEnum):
    Latitude = 'latitude'
    Longitude = 'longitude'


class BookingModel(Singleton):

    def __init__(self):
        super().__init__()
        self.collection_name = 'bookings'
        self.live_location_url = "http://localhost:8085/api/v1/find/taxi"
        self.mark_taxi_booked_url = "http://localhost:8085/api/v1/taxi/booked"
        self.mark_taxi_free_url = "http://localhost:8085/api/v1/taxi/free"
        self.notify_req =False
        self.start_location='Adayar'
        self.drop_location='Alandur'
        self.notify_cabs=[]
        self._drivers_cache = defaultdict(list) # This can be converted into Elastic Cache
        self._booking_cache = dict()



    def _get_new_booking_document( self, booking_id, user_id, user_location, destination,taxis ):
        booking_data = { 
            'booking_id' : booking_id,
            'user_id' : user_id,
            'user_location' : { 'type' : 'Point', 'coordinates' : [user_location[0], user_location[1]]},
            'destination' :{ 'type' : 'Point', 'coordinates' : [destination[0], destination[1]]},
            'status' : BookingStatus.User_Confirmed,
            'taxis' : taxis,
            'taxi_alloted' :'',
        }
        logging.info("Creating new booking request: {0}".format(booking_data['booking_id']))
        return booking_data

    def _get_status_update(self, status):
        return { 'status' : status }
    
    def _get_key( self, booking_id):
        return {'booking_id' : booking_id}
    
    def _query_location_service(self, user_location, taxi_prefer):
        logging.info(user_location)
        req_data = {LiveLocationConstants.Latitude: user_location[0], LiveLocationConstants.Longitude : user_location[1], 'taxi_prefer' : taxi_prefer}
        req_response = requests.post(self.live_location_url, json=req_data)
        # Need Response validation
        if req_response.status_code == 200:
            return req_response.json()
        else:
            logging.error("Failed to get nearby taxi: {}".format(req_response.status_code))
            return []
        
    def _mark_taxi_as_booked(self, taxi_number):
        req_data = {'taxi_number' : taxi_number}
        req_response = requests.post(self.mark_taxi_booked_url, json=req_data)
        if req_response.status_code == 200:
            logging.info("Taxi Marked as Booked")
        else:
            logging.info("Error in marking taxi as booked")

    def _mark_taxi_as_available(self, taxi_number):
        req_data = {'taxi_number' : taxi_number}
        req_response = requests.post(self.mark_taxi_free_url, json=req_data)
        if req_response.status_code == 200:
            logging.info("Taxi Marked as Available")
        else:
            logging.info("Error in marking taxi as Available")

        
    def _send_notofication_to_driver(self, booking_id, cabs,user_location,drop_location):
        logging.info("Send message to notification cache")
        # Currently we are not using Redis Cache, in future we can add it here
        for cab in cabs:
            self._drivers_cache[cab].append( booking_id )
            self._booking_cache[booking_id] = { 'user_location' : user_location, 'drop_location' : drop_location}
        

    def check_trip(self, request_data):
        cab_id = request_data.get('taxi_id')
        bookings = self._drivers_cache.get(cab_id, [])
        allBookings = []
        bookings_to_remove = []
        for booking in bookings:
            if booking in self._booking_cache:
                allBookings.append({'booking_id' : booking, 'user_location' : self._booking_cache[booking]['user_location'],
                                    'drop_location' : self._booking_cache[booking]['drop_location']})
            else:
                bookings_to_remove.append(booking)
        # Remove booking because its not there in booking cache
        for b in bookings_to_remove:
            if b in self._drivers_cache[cab_id]:
                self._drivers_cache[cab_id].remove(b)
        return allBookings
        
    #implementaition for long polling
    def get_time_to_reach_user(self, user_location, cab_location):
        logging.info("Computing time to reach from {0}-{1}".format(user_location, cab_location))
        # Approximate radius of earth in km
        Radius_Earth = 6373.0
        user_location_lat=radians(user_location[0])
        user_location_long=radians(user_location[1])
        cab_location_lat=radians(cab_location[0])
        cab_location_lon=radians(cab_location[1])
        long_distance = cab_location_lon - user_location_long
        lat_distance = cab_location_lat - user_location_lat
        area_moved = sin(lat_distance / 2) ** 2 + cos(user_location_lat) * cos(cab_location_lat) * sin(long_distance / 2) ** 2
        angle_moved = 2 * atan2(sqrt(area_moved), sqrt(1 - area_moved))
        distance_kms = Radius_Earth * angle_moved
        logging.info("Distance in Kms: %s", distance_kms)
        # Assuming Cab is going at 40Km/hr
        time_hr = (distance_kms / 40)   
        # Converting time to mins
        time_mins = (time_hr * 60)
        logging.info(int(round(time_mins)))  
        return  int(round(time_mins)) if time_mins > 1 else 1 
        # return 2
        

    def get_nearby_taxis(self, request_data):
        user_location = request_data.get(RequestConstant.User_Location)
        user_id = request_data.get(RequestConstant.User_Id)
        taxi_prefer = request_data.get(RequestConstant.Taxi_Prefer, "Any")
        logging.info("{}-{}".format(user_id,user_location))
        
        documents = self._query_location_service(user_location, taxi_prefer)
        cabs_location = []
        for document in documents:
            taxi_data = document['location']['coordinates']
            taxi_data.append(self.get_time_to_reach_user(user_location, document['location']['coordinates']))
            cabs_location.append(document['location']['coordinates'])
        
        logging.info("Found {0} cabs nearby for {1}".format(len(cabs_location), user_location))
        return { 'user_id' : user_id, 'taxis_location' : cabs_location}

    def confirm_booking(self, request_data):
        user_location = request_data.get(RequestConstant.User_Location)
        destination = request_data.get(RequestConstant.Destination)
        user_id = request_data.get(RequestConstant.User_Id)
        taxi_prefer = request_data.get(RequestConstant.Taxi_Prefer)
        # Querying the cab location again
        documents = self._query_location_service(user_location, taxi_prefer)
        cabs = []
        cab_location = {}
        for document in documents:
            cabs.append(document['taxi_number'])
            cab_location[document['taxi_number']] = document['location']['coordinates']
        # Siunce there is no cab near user location we don't need to do booking
        if len(cabs) == 0:
            return {'booking_id' : "", 'status' : BookingStatus.No_Cabs, 'taxi_alloted' : '', 
                    'user_location' : user_location, 'cab_location' : []}
        booking_id = user_id +"-" + datetime.datetime.now().strftime("%H-%M-%S")
        booking_data = self._get_new_booking_document(booking_id, user_id, user_location, destination, cabs)
        Database.get_instance().insert_single_data(self.collection_name, booking_data)
        self._send_notofication_to_driver(booking_id, cabs,user_location,destination)
        time.sleep(180) # Wait for 3 minutes
        document = Database.get_instance().get_single_data(self.collection_name, {'booking_id' : booking_id})
        logging.info(document)
        if document and document['status'] == BookingStatus.Confirm:
            return {'booking_id' : booking_id, 'status' : BookingStatus.Confirm, 'taxi_alloted' : document['taxi_alloted'], 
                    'user_location' : user_location, 'cab_location' :  cab_location.get(document['taxi_alloted'], [] )}
        else:
                # After 3 mins since no cab was found setting status to No_cabs
            update_data = self._get_status_update(BookingStatus.No_Cabs)
            update_key = self._get_key(booking_id)
            # Delete the booking from the cache
            del self._booking_cache[booking_id]
            Database.get_instance().update_single_data(self.collection_name, update_key, update_data)
            return {'booking_id' : booking_id, 'status' : BookingStatus.No_Cabs, 'taxi_alloted' : '', 
                    'user_location' : user_location, 'cab_location' : []}


    def cancel_booking(self, request_data):
        booking_id = request_data.get(RequestConstant.Booking_Id)
        if booking_id in self._booking_cache:
            del self._booking_cache[booking_id]
        if booking_id:
            update_data = self._get_status_update(BookingStatus.Cancelled)
            update_key = self._get_key(booking_id)
            Database.get_instance().update_single_data(self.collection_name, update_key, update_data)
            return { 'status' : 'Booking Deleted'} 
        else:
            logging.warn("Cancel booking request received without booking id.")
            return { 'status' : 'Booking Deleted'}
        
    def get_booking_by_id(self, request_data):
        booking_id = request_data.get(RequestConstant.Booking_Id)
        if booking_id is None:
            return {'status': False, 'Message': 'Booking ID not Exists'}
        get_key = self._get_key(booking_id)
        booking = Database.get_instance().get_single_data(self.collection_name, get_key)
        if booking is None:
            return {'status': False, 'Message': 'Booking not Exists'}
        
        return {
            'status': True,
            'Data': booking
        }

    def booking_driver_action(self, request_data):
        logging.info(request_data)
        booking_id = request_data.get('booking_id')
        taxi_id = request_data.get('taxi_id')
        status = request_data.get('status')
        query_key = self._get_key(booking_id)
        logging.info("Status: {}".format(status))
        if status == "Accept":
            document = Database.get_instance().get_single_data(self.collection_name, query_key)
            if booking_id in self._booking_cache:
                del self._booking_cache[booking_id]
            if document and document['status']==BookingStatus.User_Confirmed:
                update_data = {'taxi_alloted' : taxi_id, 'status' : BookingStatus.Confirm }
                Database.get_instance().update_single_data(self.collection_name, query_key, update_data)
                # Mark Taxi as ubooked
                self._mark_taxi_as_booked(taxi_id)
                return { 'status' : 'Confirmed', 'booking_id' : booking_id, 
                        'user_location' : document['user_location']['coordinates'],
                        'destination' : document['destination']['coordinates']}
            else:
                return { 'status' : 'Reject', 'booking_id' : booking_id, 'user_location' : [], 'destination' : []}
        else:
            if booking_id in self._drivers_cache[taxi_id]:
                logging.info("Clearing booking ID from driver Cache")
                self._drivers_cache[taxi_id].remove(booking_id)
            else:
                logging.info(self._drivers_cache)
            return { 'status' : 'Reject', 'booking_id' : booking_id, 'user_location' : [], 'destination' : []}



