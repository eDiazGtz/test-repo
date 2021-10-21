from cars_app.config.mysqlconnection import connectToMySQL

class Maker:
    # Attributes
    def __init__(self, data): # Constructor -- data expected to be DICT
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Methods
    @classmethod
    def get_all(cls):
        # query
        query = "SELECT * FROM makers;"
        # actually query DB
        results = connectToMySQL('cars_db2').query_db(query)
        # new list to append obj to
        makers = []
        # for loop
        for maker in results:
        # turn dicts into obj
            makers.append(cls(maker))
        # return new list of obj
        return makers
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO makers (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());"
        return connectToMySQL('cars_db2').query_db(query, data)