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

    init = {} # temp value to enter into the while loop
    col3 = connect('db','meta')
    # main function to download all data
    col3.drop() # à enlever ? 
    id_list = get_id(col)
    base_url = "https://www.youtube.com/watch?v="
    
    # log = MyLogger()
    ydl_opts = {}
    # ydl_opts['logger'] = log
    failed_videos=[]
    count_line=0
    # logger_filename= 'logger_'+datetime.datetime.today().strftime('%Y-%m-%d')
    # lf= pd.read_csv(logger_filename)
    print(len(id_list))
    for elt in id_list : # loop through all id
        try:
            print (elt)
            working_url = base_url + elt["id"] # create a link with base_url and the id
            # downloading meta data for the video
            with youtube_dl.YoutubeDL(ydl_opts) as ydl :
                meta = ydl.extract_info(working_url,download=False)
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

        except Exception as err:

            failed_videos.append({'id':elt,'error':str(err)})
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
