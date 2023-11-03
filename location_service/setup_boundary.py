from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point


proj_wgs84 = pyproj.Proj('+proj=latlon +datum=WGS84')


class BoundaryService:

# To find the latitude and longitude along the circle for a given km radius from the given point

    def geodesic_point_buffer(self, lat, lon, km):
    # Azimuthal equidistant projection
        aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
        project = partial(
            pyproj.transform,
            pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
            proj_wgs84)
        buf = Point(0, 0).buffer(km * 1000)  # distance in metres
        return transform(project, buf).exterior.coords[:]

# To find the min/mx latitude and longitude from the above list of values

    def minmaxcoordinates(self,coordinate_list):
        min_lat = min(coordinate_list, key=lambda i: i[1])[1]
        max_lat = max(coordinate_list, key=lambda i: i[1])[1]
        min_lon = min(coordinate_list, key=lambda i: i[0])[0]
        max_lon = max(coordinate_list, key=lambda i: i[0])[0]
        minmaxvalue=[]
        minmaxvalue.append(min_lat)
        minmaxvalue.append(max_lat)
        minmaxvalue.append(min_lon)
        minmaxvalue.append(max_lon)
        return minmaxvalue
