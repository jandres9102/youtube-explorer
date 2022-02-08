from __future__ import unicode_literals
from database import *
from lecteur import *
import os 
import json 
import youtube_dl 

#reading of meta-key
with open("meta-key.txt",'r') as kaka :
    l = kaka.readlines()
meta_key = [k.strip('\n') for k in l]

db, col3 = connect('db','meta')
# main function to download all data 
col3.drop()

def main(): 
    id_list = get_id(col)
    base_url = "https://www.youtube.com/watch?v="
    ydl_opts = {}
    failed_videos=[]
    for elt in id_list : # loop through all id
        try:
            working_url = base_url + elt["id"] # create a link with base_url and the id 
            # downloading meta data for the video
            with youtube_dl.YoutubeDL(ydl_opts) as ydl : 
                meta = ydl.extract_info(working_url,download=False)
            temp_dict = dict()
            for key in meta_key:
                if key not in meta.keys():
                    temp_dict[key]=None
                else:
                    temp_dict[key]=meta[key]   
            store_data(col3,temp_dict)
                
            # put the meta data 
        except Exception as err:
            failed_videos.append({'id':elt,'error':str(err)})

    # print(list(col3.find()))
    return 0

if __name__ == "__main__" : 
    main()


