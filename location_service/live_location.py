from utils import Singleton, Database

class UsersMixin(object):

    def get_by_number( self, taxi_number):
        query = {'taxi_number': taxi_number}
        return Database.get_instance().get_single_data(self.collection_name, query)

class LiveLocation(UsersMixin, Singleton):

    def __init__( self ):
        super().__init__()
        self.collection_name = 'livelocation'

    def get_count_key(self, key):
        count_key = Database.get_instance().count_documents(self.collection_name,key)
        return count_key

    def ins(self, loc_data):
        return Database.get_instance().insert_single_data(self.collection_name, loc_data)

    def upd_loc(self, key_filter, key_update):
        return Database.get_instance().update_single_data(self.collection_name, key_filter,key_update)

def main():
    # Checkling SingleTon for each
    print(LiveLocation.get_instance())

if __name__ == "__main__":
    main()