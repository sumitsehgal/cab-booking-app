from math import radians, cos, sin, asin, sqrt

from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point


# Calculate Distance between two Locations
def distance(lat1, lat2, lon1, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return (c * r)


def geodesic_point_buffer(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
        proj_wgs84)
    buf = Point(0, 0).buffer(km * 1000)  # distance in metres
    return transform(project, buf).exterior.coords[:]


if __name__ == "__main__":

    # driver code
    # Test Distance Calculation Code
    lat1 = 13.078
    lat2 = 13.083
    lon1 = 80.2875
    lon2 = 80.33
    print(distance(lat1, lat2, lon1, lon2), "K.M")

    # Test: Define Boundary
    proj_wgs84 = pyproj.Proj('+proj=latlon +datum=WGS84')

    b = geodesic_point_buffer(13.0798, 80.2846, 5.0)
    for x in b:
        print (x)
    res = min(b, key = lambda i : i[1])[1]
    print (res)

