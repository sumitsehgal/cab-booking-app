import random

from bson import ObjectId
import livelocation
from get_point_at_distance import GetPointAtDistance



class LiveLocationService:

    # To update the live location of a taxi on the Live Location Collection
    def updliveloc(self,taxiid,minmaxlatlon):
        minlat = minmaxlatlon[0]
        maxlat = minmaxlatlon[1]
        minlon = minmaxlatlon[2]
        maxlon = minmaxlatlon[3]
        key = {"taxi_number": taxiid}
        liveloc= livelocation.LiveLocation()
        taxi_count = liveloc.get_count_key(key)
        if taxi_count == 0:
            new_lat = random.uniform(minlat, maxlat)
            new_long = random.uniform(minlon, maxlon)
            loc_data = {
            'taxi_number': taxiid,
            'live_location': {
            'type': "Point",
            'coordinates': [new_lat, new_long]
            }
            }
            liveloc.ins(loc_data)
        else:
            doc_select_loc = liveloc.get_by_number(taxiid)
            # Call function to get the new location based on 2 kms movement in North direction
            id = doc_select_loc['_id']
            curr_lat = doc_select_loc['live_location']['coordinates'][0]
            curr_long = doc_select_loc['live_location']['coordinates'][1]
            distance = 2  # 2 kms movement
            bearing = 90  # 90 degrees direction
            getpointatdistance=GetPointAtDistance()
            new_lat, new_long = getpointatdistance.get_point_at_distance(curr_lat, curr_long, distance, bearing)
            key_filter={"_id" : ObjectId(id)}
            key_update={"$set" : {"live_location": {'type': "Point",'coordinates': [new_lat,new_long]}}}
            liveloc.upd_loc(key_filter, key_update)