from __future__ import unicode_literals
import youtube_dl 
from pymongo import MongoClient # import to communicate with de Mongo database 

# function to connect to the database
def connect(login,password):
    pass 

# function to retrieve video's id 
def get_id():
    pass 
# function to store date in the Mongo database 
def store_data():
    pass 

# main function to download all data 
def main(): 
    id_list = get_id()
    base_url = "https://www.youtube.com/watch?v="
    ydl_opts = {}
    for elt in id_list : # loop through all id 
        working_url = base_url + elt # create a link with base_url and the id 
        # downloading meta data for the video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl : 
            meta = ydl.extract_info(working_url,download=False)
        # put the meta data 
    
    return 0

if __name__ == "__main__" : 
    main()