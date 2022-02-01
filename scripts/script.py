from __future__ import unicode_literals
from database import *
import os 
import json 

# main function to download all data 
def main(): 
    id_list = get_id()
    base_url = "https://www.youtube.com/watch?v="
    ydl_opts = {}
    failed_videos=[]
    for elt in id_list : # loop through all id
        try:
            working_url = base_url + elt # create a link with base_url and the id 
            # downloading meta data for the video
            with youtube_dl.YoutubeDL(ydl_opts) as ydl : 
                meta = ydl.extract_info(working_url,download=False)
            # put the meta data 
        except Exception as err:
            failed_videos.append({'id':elt,'error':str(err)})
    
    return 0

if __name__ == "__main__" : 
    main()
