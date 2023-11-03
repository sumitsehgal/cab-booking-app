from setup_boundary import BoundaryService
from user_service.users import Taxis
from update_live_location import LiveLocationService

def main():

    # Instantiate BoundaryService to calculate the boundary
    boundary_service = BoundaryService()
    ## Pass Latitude, Long and radius to get the Latitude and longitude coordinates along the given radius
    boundarypoints = boundary_service.geodesic_point_buffer(13.0798, 80.2846, 20.0)

    ### To Define the boundary using a specific Latitude and Longitude
    minmaxlatlon = boundary_service.minmaxcoordinates(boundarypoints)

    ## to get all the taxis from the taxi collection
    taxis = Taxis()
    taxis_collection=taxis.get_all()

    # for each taxi update the live location
    for taxi in taxis_collection:
        taxiid = taxi['taxi_number']
        live_location=LiveLocationService()
        live_location.updliveloc(taxiid,minmaxlatlon)

if __name__ == "__main__":
    main()