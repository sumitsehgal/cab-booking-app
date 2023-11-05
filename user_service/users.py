import select
from utils import Singleton, Database
from datetime import datetime


class UsersMixin(object):

    def get_list_with_pagination(self, key = {}, page = 1, limit = 10):
        offset = (page - 1) * limit
        return Database.get_instance().paginated_list(self.collection_name, key, offset, limit)
        
    def add(self, first_name, middle_name, last_name, mobile_number, city, emergency_contact = None):
        try:
            # Basic Validation to Generate Unique User ID
            if first_name.strip() == '' or mobile_number.strip() == '':
                raise ValueError("First Name and Mobile Number are required!")
            
            # Registered on Date
            current_datetime = datetime.now()
        
            # User Dictionary
            user_data = {   
                            'first_name' : first_name,
                            'middle_name' : middle_name,
                            'last_name' : last_name,
                            'mobile_number': mobile_number,
                            'city': city,
                            'user_id': first_name + "-" + str(mobile_number),
                            'emergency_contact': emergency_contact,
                            'registered_on': current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                        }
            
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
            selected_cols = ['first_name', 'last_name', 'middle_name', 'mobile_number', 'city', 'emergency_contact', 'last_edited_on']

             # Last Edited
            current_datetime = datetime.now()
            user_data['last_edited_on'] = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            # Remove None values from the update data
            user_data = {k: v for k, v in user_data.items() if v is not None and k in selected_cols}  

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

    def add(self, taxi_number, taxi_type, city, driver = None, year_of_manufacturing = None, seating_capacity = None, availability_status = 'Available', fuel_type='Petrol' ):

        try:
             # Basic Validation to Generate Unique User ID
            if taxi_number.strip() == '' or taxi_type.strip() == '':
                raise ValueError("Taxi Number and Taxi Type are required!")
            
            # Registered on Date
            current_datetime = datetime.now()

            user_data = {
                            'taxi_number' : taxi_number, # this should be unique
                            'taxi_type' : taxi_type,
                            'city' : city,
                            'driver' : driver if driver else '',
                            'year_of_manufacturing': year_of_manufacturing,
                            'seating_capacity': seating_capacity,
                            'availability_status': availability_status,
                            'fuel_type': fuel_type,
                            'registered_on': current_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                            'taxi_id': taxi_type+'-'+taxi_number
                        }
            # Insert into Collection
            inserted_id = Database.get_instance().insert_single_data(self.collection_name, user_data)
            # User User ID
            return user_data['taxi_id']
        except Exception as e:
            print(f"Error adding user: {e}")
            return None
    
    def get_by_type( self, taxi_type):
        query = { 'taxi_type' : taxi_type}
        return Database.get_instance().get_multiple_data(self.collection_name, query)
    
    def get_by_number( self, taxi_number):
        query = {'taxi_number': taxi_number}
        return Database.get_instance().get_single_data(self.collection_name, query)
    
    def get_by_id( self, taxi_id):
        query = {'taxi_id': taxi_id}
        return Database.get_instance().get_single_data(self.collection_name, query)
    
    def get_all(self):
        return Database.get_instance().get_all_records(self.collection_name)
    
    def edit(self, taxi_id, taxi_data):
        try:
            # Basic Validation to Generate Unique Taxi ID
            if 'taxi_number' not in taxi_data or 'taxi_type' not in taxi_data:
                raise ValueError("Taxi Number and Taxi Type are required!")
            
            key = {'taxi_id': taxi_id}
            selected_cols = ['taxi_number', 'taxi_type', 'city', 'driver', 'year_of_manufacturing', 'seating_capacity', 'availability_status', 'fuel_type', 'last_edited_on']

             # Last Edited
            current_datetime = datetime.now()
            taxi_data['last_edited_on'] = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            # Remove None values from the update data
            taxi_data = {k: v for k, v in taxi_data.items() if v is not None and k in selected_cols}  

            # Update into Collection
            document = Database.get_instance().update_single_data(self.collection_name, key, taxi_data)
            # Taxi ID
            return taxi_id
        except Exception as e:
            print(f"Error updating taxi: {e}")
            return None
        
    def delete_by_id(self, taxi_id):
        return Database.get_instance().delete_single_data(self.collection_name, {'taxi_id':taxi_id})
    



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