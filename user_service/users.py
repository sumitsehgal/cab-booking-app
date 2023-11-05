from utils import Singleton, Database
from datetime import datetime


class UsersMixin(object):

    def get_list_with_pagination(self, key = {}, page = 1, limit = 10):
        offset = (page - 1) * limit
        return Database.get_instance().paginated_list(self.collection_name, key, offset, limit)
        
    def add(self, user_data):
        try:
            # Basic Validation to Generate Unique User ID
            if 'first_name' not in user_data or 'mobile_number' not in user_data:
                raise ValueError("First Name and Mobile Number are required!")
            
            # Unique User ID
            user_data['user_id'] = user_data['first_name'] + "-" + str(user_data['mobile_number'])
            
            # TODO: Need to Discuss to Move it to Class wise because Driver has onboarding_on etc
            # Registered on Date
            current_datetime = datetime.now()
            user_data['registered_on'] = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            # Insert into Collection
            inserted_id = Database.get_instance().insert_single_data(self.collection_name, user_data)
            # User User ID
            return user_data['user_id']
        except Exception as e:
            print(f"Error adding user: {e}")
            return None
        

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

    def delete_by_id(self, user_id):
        return Database.get_instance().delete_single_data(self.collection_name, {'user_id':user_id})
    
    def edit(self, user_id, user_data):
        try:
            # Basic Validation to Generate Unique User ID
            if 'first_name' not in user_data or 'mobile_number' not in user_data:
                raise ValueError("First Name and Mobile Number are required!")
            
            key = {'user_id': user_id}

            # Remove None values from the update data
            user_data = {k: v for k, v in user_data.items() if v is not None}  

            # Last Edited
            current_datetime = datetime.now()
            user_data['last_edited_on'] = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            # Update into Collection
            document = Database.get_instance().update_single_data(self.collection_name, key, user_data)
            # User User ID
            return user_data['user_id']
        except Exception as e:
            print(f"Error updating user: {e}")
            return None


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

    def add(self, json_data ):
        user_data = {
                        'taxi_id' : json_data.get('taxi_id'), # this should be unique
                        'taxi_type' : json_data.get('taxi_type'),
                        'city' : json_data.get('city'),
                        'driver' : json_data.get('driver', '') 
                    }
        return Database.get_instance().insert_single_data(self.collection_name, user_data)
    
    def get_by_type( self, taxi_type):
        query = { 'taxi_type' : taxi_type}
        return Database.get_instance().get_multiple_data(self.collection_name, query)
    
    def get_by_number( self, taxi_number):
        query = {'taxi_id': taxi_number}
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