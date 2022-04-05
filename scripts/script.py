from __future__ import unicode_literals
from database import *
from lecteur import *
from bs4 import BeautifulSoup
import urllib
import re
from logger import MyLogger
import pandas as pd
import json
import youtube_dl
import datetime
import os



file_path = "image/"
# function to download the vignette
def download_json(youtube_id):
    # Téléchargement du contenu HTML de la page
    response = urllib.request.urlopen('https://www.youtube.com/watch?v=' + youtube_id)
    htmlContent = response.read().decode('UTF-8')


    # Extraction du contenu de la variable ytInitialPlayerResponse
    soup = BeautifulSoup(htmlContent, "html.parser")
    pattern = re.compile(r"^var ytInitialPlayerResponse = (.*?);$", re.MULTILINE | re.DOTALL)
    script = soup.find("script", text=pattern)

    ytInitialPlayerResponse = json.loads(pattern.search(script.text).group(1))


    oRes = {}

    oRes['title']= ytInitialPlayerResponse['videoDetails']['title']
    oRes['video_duration']= int(ytInitialPlayerResponse['videoDetails']['lengthSeconds'])

    tmpParams = ytInitialPlayerResponse['storyboards']['playerStoryboardSpecRenderer']['spec'].split("|")

    base_url = tmpParams[0]
    tmpParams = tmpParams[1:]

    storyboards = []
    for i in range(len(tmpParams)):
        tmp_url = base_url.replace("$L", str(i))
        tmpSbInfo = tmpParams[i].split("#")
        sbInfo = {}
        sbInfo['sub_image_width'] = int(tmpSbInfo[0])
        sbInfo['sub_image_height'] = int(tmpSbInfo[1])
        sbInfo['nb_total_sub_image'] = int(tmpSbInfo[2])
        sbInfo['nb_col_by_image'] = int(tmpSbInfo[3])
        sbInfo['nb_row_by_image'] = int(tmpSbInfo[4])
        if int(tmpSbInfo[5]) == 0:
            sbInfo['time_in_between'] = (oRes['video_duration']*1000)//sbInfo['nb_total_sub_image']
        else:
            sbInfo['time_in_between'] = int(tmpSbInfo[5])
        image_file_name = tmpSbInfo[6]
        sigh = tmpSbInfo[7]
        
        tmp_url = tmp_url.replace("$N", image_file_name) + "&sigh=" + sigh

        images = []
        nb_image = 0
        nb_sub_images = 0
        while nb_image*(sbInfo['nb_col_by_image']*sbInfo['nb_row_by_image']) < sbInfo['nb_total_sub_image']:
            image = {}
            image['url'] = tmp_url.replace("$M", str(nb_image))
            sub_images = []
            for row in range(sbInfo['nb_row_by_image']):
                if(nb_sub_images > sbInfo['nb_total_sub_image']):
                    continue
                for col in range(sbInfo['nb_col_by_image']):
                    if(nb_sub_images > sbInfo['nb_total_sub_image']):
                        continue
                    sub_image = {}
                    sub_image['timecode'] = nb_sub_images*sbInfo['time_in_between']//1000
                    crop={}
                    crop['x_start'] = sbInfo['sub_image_width']*col
                    crop['x_end'] = sbInfo['sub_image_width']*(col + 1)
                    crop['y_start'] = sbInfo['sub_image_height']*row
                    crop['y_end'] = sbInfo['sub_image_height']*(row + 1)
                    sub_image['crop'] = crop
                    sub_images.append(sub_image)
                    nb_sub_images = nb_sub_images + 1
                    
            image['sub_images'] = sub_images
            images.append(image)
            nb_image = nb_image + 1
        sbInfo['images'] = images
        storyboards.append(sbInfo)
        
    oRes['storyboards'] = storyboards
    return oRes

def download_vignette(oRes):
    file_name = oRes["title"]
    print(oRes["title"]+" depuis la fonction")
    count = 0 
    for elt in oRes['storyboards'][2]['images']:
        urllib.request.urlretrieve(elt['url'],"image/"+file_name+"-"+str(count)+".png")
        count +=1
    print(os.listdir("image"))

# main function to download youtube meta and the vignette
def main():
    #reading of meta-key
    with open("scripts/meta-key.txt",'r') as f :
        l = f.readlines()
    meta_key = [k.strip('\n') for k in l]

    col3 = connect('db','meta')
    col = connect('db','id')
    # main function to download all data
    col3.drop() # à enlever ? 
    base_url = "https://www.youtube.com/watch?v="


    ydl_opts = {'outtmpl': './video/%(title)s.%(ext)s'} # replace './downloadedsongs/' by another path  

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
                    meta = ydl.extract_info(working_url,download=False)
                temp_dict = dict()
                # keep only the needed data
                for key in meta_key:
                    if key not in meta.keys():
                        temp_dict[key]=None
                    else:
                        temp_dict[key]=meta[key]
                
                temp_dict['date'] = datetime.datetime.today().strftime('%Y/%m/%d') # add date to know when the data was downloaded 
                oRes = download_json(elt["id"])
                temp_dict['vignette'] =  oRes
                download_vignette(oRes)
                # add those data to the db 
                store_data(col3,temp_dict)
                update_data(col,elt['id'],"status_video","1") # say we only downloaded the video
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
