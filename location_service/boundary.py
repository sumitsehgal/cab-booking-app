from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point


proj_wgs84 = pyproj.Proj('+proj=latlon +datum=WGS84')

class BoundaryHelper:

    def __init__(self, lat, lon, km):
        self._lat = lat
        self._lon = lon
        self._km = km
        self._service_area = self.__get_service_area()
        self.set_min_max_for_service()

    # To find the latitude and longitude along the circle for a given km radius from the given point
    def __get_service_area(self):
        """
        Get all the latiitude and longitude in the boundary defined
        """
    # Azimuthal equidistant projection
        aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
        project = partial(
            pyproj.transform,
            pyproj.Proj(aeqd_proj.format(lat=self._lat, lon=self._lon)),
            proj_wgs84)
        buf = Point(0, 0).buffer(self._km * 1000)  # distance in metres
        return transform(project, buf).exterior.coords[:]
    
    def set_min_max_for_service(self):
        self.min_lat = min(self._service_area, key=lambda i:i[1])[1]
        self.min_lon = min(self._service_area, key=lambda i:i[0])[0]
        self.max_lat = max(self._service_area, key=lambda i: i[1])[1]
        self.max_lon = max(self._service_area, key=lambda i: i[0])[0]

    def is_in_service_boundary(self, lan, lon):
        # This needs to return True if the lan and lon is in service area
        # False if lan and lon is outside service area
        if( (lan,lon) in self._service_area):
            return True
        else:
            return False
        
    def min_max_coordinates(self):
        return { 'min_latitude' : self.min_lat, 
                 'max_latitude' : self.max_lat,
                 'min_longitude' : self.min_lon, 
                 'max_longitude': self.max_lon
                }
        
def main():
    import geocoder
    my_location = geocoder.ip('me')
    bs = BoundaryHelper(my_location.latlng[0], my_location.latlng[1], 5)
    print(bs.geodesic_point_buffer())

if __name__ == "__main__":
    main()
