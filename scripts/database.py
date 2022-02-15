from pymongo import MongoClient # import to communicate with de Mongo database 


client = MongoClient(host="db",port=27017)

# function to connect to the database
def connect(db_name,col_name):
    db = client[db_name]
    col = db[col_name]
    return db,col

# function to retrieve video's id 
def get_id(col):
    id_list = list(col.find({},{"id":1,"_id":0}))
    return id_list
    

    
# function to store date in the Mongo database 
def store_data(col,insert_values):
    col.insert_one(insert_values)




