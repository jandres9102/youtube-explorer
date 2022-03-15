from __future__ import unicode_literals
from database import *
from lecteur import *
from logger import MyLogger
import pandas as pd
import os
import json
import youtube_dl
import datetime
import time


def main():
    #reading of meta-key
    with open("scripts/meta-key.txt",'r') as f :
        l = f.readlines()
    meta_key = [k.strip('\n') for k in l]

    init = {'_id': "init_value", 'id': 'init_value', 'status': 'init_value'} # temp value to enter into the while loop
    col3 = connect('db','meta')
    col = connect('db','id')
    # main function to download all data
    col3.drop() # à enlever ? 
    id_list = get_id(col)
    base_url = "https://www.youtube.com/watch?v="

    ydl_opts = {'outtmpl': './video/%(title)s.%(ext)s'} # replace './downloadedsongs/' by another path  

    failed_videos=[]
    # count the number of video to process 
    line_to_process = col.count_documents({'status_video':"0"})
    
    # count_line=0
    # logger_filename= 'logger_'+datetime.datetime.today().strftime('%Y-%m-%d')
    # lf= pd.read_csv(logger_filename)
    # print(len(id_list))

    while line_to_process > 0:
        # access to a random data from the database (should limit functions that try to acess to the same value )
        elt = list(col.aggregate([{ "$sample": { "size": 1 } }]))[0]
        update_data(col,elt['id'],"label",1)
        if elt["status_video"] == "0" and elt["label"] == 0:
            try:
                working_url = base_url + elt["id"] # create a link with base_url and the id
                # downloading meta data for the video
                with youtube_dl.YoutubeDL(ydl_opts) as ydl :
                    meta = ydl.extract_info(working_url,download=True)
                temp_dict = dict()
                # keep only the needed data
                for key in meta_key:
                    if key not in meta.keys():
                        temp_dict[key]=None
                    else:
                        temp_dict[key]=meta[key]
                
                temp_dict['date'] = datetime.datetime.today().strftime('%Y/%m/%d') # add date to know when the data was downloaded 
                # add those data to the db 
                store_data(col3,temp_dict)
                # updtading the video status 
                update_data(col,elt['id'],"status_video","1") # say we only downloaded the video
                # if elt['status'] == "ongoing" : # case there was no processing on this video
                #     update_data(col,elt['id'],"status","ongoing_video") # say we only downloaded the video
                # elif elt['status'] == "ongoing_commentaire" : # case comment where processed
                #     update_data(col,elt['id'],"status","done") # as we downloaded the video we put done here 
            except :
                update_data(col,elt['id'],"status_video","2")

        # update the remainig value to process 
        line_to_process = col.count_documents({'status_video':"0"}) 
       
        #     print('faillllllllllllllllllllllllllllllllllllll'+log.get_error_msg())
        # lf['last_inspection_date'][count_line] = time.time()
        # lf['debug_msg'][count_line] = log.get_debug_msg()
        # lf['warning_msg'][count_line] = log.get_warning_msg()
        # lf['error_msg'][count_line] = log.get_error_msg()
        # count_line = count_line+1
        # if (count_line%10 == 0):
        #     lf.to_csv(logger_filename, index=False)
        #     print('tesr')
        # print(log.get_all_msg())
        # log.reset()
    # print(list(col3.find()))
    return 0


if __name__ == "__main__" :
    main()
