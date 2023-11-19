import random

from bson import ObjectId
from get_point_at_distance import GetPointAtDistance
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import logging

TAXIS = [
    ['Taxi-11',  21.16107863,    79.08568417],
    ['Taxi-12',  21.16154888,    79.08598994],
    ['Taxi-13',  21.16190157,    79.08476149],
    ['Taxi-14',  21.16199162,    79.08556615],
    ['Taxi-15',  21.16146133,    79.08536231],
    ['Taxi-16',  21.16048831,    79.08719694],
    ['Taxi-17',  21.16095856,    79.08718621],
    ['Taxi-18',  21.16051832,    79.08672487],
    ['Taxi-19',  21.16113366,    79.08811425],
    ['Taxi-110', 21.1606634,     79.08619916],
    ['Taxi-111', 21.16049956,    79.08445304],
    ['Taxi-112', 21.16042953,    79.08502703],
    ['Taxi-113', 21.16050457,    79.08446377],
    ['Taxi-114', 21.15999679,    79.08435648],
    ['Taxi-115', 21.15959657,    79.08460056],
    ['Taxi-116', 21.15913632,    79.08391928],
    ['Taxi-117', 21.15882115,    79.08406948],
    ['Taxi-118', 21.15861603,    79.08480172],
    ['Taxi-119', 21.15948651,    79.08483928],
    ['Taxi-120', 21.15962659,    79.08434307],
    ['Taxi-121', 21.15787062,    79.08500021],
    ['Taxi-122', 21.15723526,    79.08524965],
    ['Taxi-123', 21.15719524,    79.08479368],
    ['Taxi-124', 21.15801069,    79.0840212],
    ['Taxi-125', 21.15678751,    79.08520137],
    ['Taxi-126', 21.15720524,    79.0833426],
    ['Taxi-127', 21.1569501,     79.08323531],
    ['Taxi-128', 21.15683503,    79.08297782],
    ['Taxi-129', 21.15628472,    79.08344184],
    ['Taxi-130', 21.15645232,    79.0846998],
    ['Taxi-131', 21.15679907,    79.06868009],
    ['Taxi-132', 21.15361723,    79.06829385],
    ['Taxi-133', 21.15287679,    79.07357244],
    ['Taxi-134', 21.15675905,    79.07526759],
    ['Taxi-135', 21.15029524,    79.07455949],
    ['Taxi-136', 21.15593858,    79.07902269],
    ['Taxi-137', 21.1527167,     79.0789154],
    ['Taxi-138', 21.15031525,    79.07951621],
    ['Taxi-139', 21.15307691,    79.08258466],
    ['Taxi-140', 21.15257662,    79.076834],
    ['Taxi-141', 21.12625361,    79.06363753],
    ['Taxi-142', 21.12120962,    79.05436782],
    ['Taxi-143', 21.11224212,    79.05668525],
    ['Taxi-144', 21.10791831,    79.08020286],
    ['Taxi-145', 21.12913581,    79.07659797],
    ['Taxi-146', 21.08803916,    79.11895541],
    ['Taxi-147', 21.08583687,    79.13393287],
    ['Taxi-148', 21.08996112,    79.12384776],
    ['Taxi-149', 21.07934995,    79.13187293],
    ['Taxi-150', 21.08370048,    79.12618887]
]
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
    for taxi_number, new_lat, new_lon in TAXIS:
        loc_data = {
            'taxi_number' : taxi_number,
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
    initialize_taxi_location()
    #mock_live_update()
    #mock_taxi_free_booked()

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
