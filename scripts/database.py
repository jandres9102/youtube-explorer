from pymongo import MongoClient # import to communicate with de Mongo database 




# function to connect to the database
def connect(db_name,col_name,host="db",port=27017):
    client = MongoClient(host,port)
    db = client[db_name]
    col = db[col_name]
    return col

# function to retrieve video's id 
def get_id(col):
    id_list = list(col.find({},{"id":1,"_id":0}))
    return id_list
    

    
# function to store date in the Mongo database 
def store_data(col,insert_values):
    col.insert_one(insert_values)

# function to updtate a given value in the Mongo database 
def update_data(col,video_id,field,value):
    col.find_one_and_update({"id" : video_id},{"$set" : {field:value}},upsert=True)


