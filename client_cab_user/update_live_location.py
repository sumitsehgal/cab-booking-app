import random

from bson import ObjectId
from get_point_at_distance import GetPointAtDistance
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import logging


def get_all_taxis():
    req_url = 'http://localhost:8080/api/v1/taxi'
    req_response = requests.get(req_url,timeout=120)
    all_taxis = req_response.json()
    return { doc['taxi_number']: doc for doc in all_taxis['Data'] }

def get_boundary_cordinates():
    req_url = 'http://localhost:8085/api/v1/boundary/cordinates'
    req_response = requests.get(req_url,timeout=120)
    return  req_response.json()
    
def send_data_to_server(loc_data):
    req_url = 'http://localhost:8085/api/v1/taxi/update'
    req_response = requests.post(req_url, json = loc_data)
    print(req_response.json()['Status'])

def initialize_taxi_location():
    taxis = get_all_taxis()
    boundary = get_boundary_cordinates()
    min_lat = boundary['min_latitude']
    max_lat = boundary['max_latitude']
    min_lon = boundary['min_longitude']
    max_lon = boundary['max_longitude']
    for taxi_number, taxi in taxis.items():
        new_lat = random.uniform(min_lat, max_lat)
        new_lon = random.uniform(min_lon, max_lon)
        loc_data = {
            'taxi_number' : taxi['taxi_number'],
            'latitude': new_lat,
            'longitude' : new_lon
        }
        send_data_to_server(loc_data)

def update_and_send(taxi):
    taxi_number = taxi['taxi_number']
    req_url = 'http://localhost:8085/api/v1/taxi/{}'.format(taxi_number)
    taxi_loc = requests.get(req_url).json()
    curr_lat = taxi_loc['latitude']
    curr_lon = taxi_loc['longitude']
    distance = 0.5
    bearing = random.choice([85, 86, 87, 88, 89,90])
    getpointatdistance=GetPointAtDistance()
    new_lat, new_lon = getpointatdistance.get_point_at_distance(curr_lat, curr_lon, distance, bearing)
    print("Moving {0} from ({1},{2}) to ({3},{4})".format(taxi['taxi_number'], curr_lat, curr_lon, new_lat, new_lon))
    loc_data = {
        'taxi_number' : taxi['taxi_number'],
        'latitude' : new_lat,
        'longitude' : new_lon
    }
    send_data_to_server(loc_data)


def mock_live_update():
    print("Starting Live Updates")
    taxis = get_all_taxis()
    print("Number of Taxis:{0}".format(len(taxis)))
    boundary = get_boundary_cordinates()
    min_lat = boundary['min_latitude']
    max_lat = boundary['max_latitude']
    min_lon = boundary['min_longitude']
    max_lon = boundary['max_longitude']

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        while True:
            for taxi_number, taxi in taxis.items():
                is_moving = random.choice([0,1])
                if is_moving:
                    futures.append(executor.submit(update_and_send, taxi))
            is_complete = False
            while is_complete==False:
                is_all_done = True
                for f in futures:
                    if not f.done():
                        is_all_done = False
                if is_all_done:
                    is_complete = True

            time.sleep(120) # sleeping for 2 mins


def mock_taxi_free_booked():
    req_url = 'http://localhost:8085/api/v1/taxi/booked'
    req_data = {'taxi_number' : 'Taxi-138'}
    req_response = requests.post(req_url, json = req_data)
    print(req_response.json())
    req_url = 'http://localhost:8085/api/v1/taxi/free'
    req_response = requests.post(req_url, json = req_data)
    print(req_response.json())


def main():
    #initialize_taxi_location()
    #mock_live_update()
    mock_taxi_free_booked()

if __name__ == "__main__":
    main()
    
# class LiveLocationService:

#     # To update the live location of a taxi on the Live Location Collection
#     def updliveloc(self,taxiid,minmaxlatlon):
#         minlat = minmaxlatlon[0]
#         maxlat = minmaxlatlon[1]
#         minlon = minmaxlatlon[2]
#         maxlon = minmaxlatlon[3]
#         key = {"taxi_number": taxiid}
        
#         taxi_count = liveloc.get_count_key(key)
#         if taxi_count == 0:
#             new_lat = random.uniform(minlat, maxlat)
#             new_long = random.uniform(minlon, maxlon)
#             loc_data = {
#             'taxi_number': taxiid,
#             'location': {
#                 'type': "Point",
#                 'coordinates': [28.67423, 77.23172]
#                 }
#             }
#             liveloc.ins(loc_data)
#         else:
#             doc_select_loc = liveloc.get_by_number(taxiid)
#             # Call function to get the new location based on 2 kms movement in North direction
#             id = doc_select_loc['_id']
#             curr_lat = doc_select_loc['live_location']['coordinates'][0]
#             curr_long = doc_select_loc['live_location']['coordinates'][1]
#             distance = 2  # 2 kms movement
#             bearing = 90  # 90 degrees direction
#             getpointatdistance=GetPointAtDistance()
#             new_lat, new_long = getpointatdistance.get_point_at_distance(curr_lat, curr_long, distance, bearing)
#             key_filter={"_id" : ObjectId(id)}
#             key_update={"$set" : {"live_location": {'type': "Point",'coordinates': [new_lat,new_long]}}}
#             liveloc.upd_loc(key_filter, key_update)