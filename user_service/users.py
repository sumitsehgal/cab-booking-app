from utils import Singleton, Database


class UsersMixin(object):
    def add(self, first_name, middle_name, last_name, mobile_number,city):
        user_data = {   
                        'first_name' : first_name,
                        'middle_name' : middle_name,
                        'last_name' : last_name,
                        'mobile_number': mobile_number,
                        'city': city,
                        'user_id': first_name + "-" + str(mobile_number) #trying to form the unique key
                    }
        Database.get_instance().insert_single_data(self.collection_name, user_data)
        

    def get_by_name(self, first_name, middle_name = None, last_name = None):
        query = { 'first_name' : first_name }
        if middle_name:
            query['middle_name']=middle_name
        if last_name:
            query['last_name']:last_name

        return Database.get_instance().get_multiple_data(self.collection_name, query)

    def get_by_id(self, user_id):
        return Database.get_instance().get_single_data(self.collection_name, {'user_id':user_id})
    
    def get_all( self ):
        return Database.get_instance().get_all_records(self.collection_name)

    # Need to implement delete user
    # need to implement updating data


class Users(UsersMixin, Singleton):
    
    def __init__(self) -> None:
        super().__init__()
        self.collection_name = 'users'

    
class Drivers(UsersMixin,Singleton):
    
    def __init__(self) -> None:
        super().__init__()
        self.collection_name = 'drivers'

class Taxis(UsersMixin, Singleton):

    def __init__( self ):
        super().__init__()
        self.collection_name = 'taxis'

    def add(self, taxi_number, taxi_type, city, driver = None ):
        user_data = {
                        'taxi_number' : taxi_number, # this should be unique
                        'taxi_type' : taxi_type,
                        'city' : city,
                        'driver' : driver if driver else ''
                    }
        return Database.get_instance().insert_single_data(self.collection_name, user_data)
    
    def get_by_type( self, taxi_type):
        query = { 'taxi_type' : taxi_type}
        return Database.get_instance().get_multiple_data(self.collection_name, query)
    
    def get_by_number( self, taxi_number):
        query = {'taxi_number': taxi_number}
        return Database.get_instance().get_single_data(self.collection_name, query)
    
    def get_all(self):
        return Database.get_instance().get_all_records(self.collection_name)


def main():
    # Checkling SingleTon for each 
    print(Users.get_instance())
    print(Drivers.get_instance())
    print(Taxis.get_instance())

    print(Users.get_instance())
    print(Drivers.get_instance())
    print(Taxis.get_instance())

if __name__ == "__main__":
    main()