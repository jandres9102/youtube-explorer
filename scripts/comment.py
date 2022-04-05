import os, json 
from database import *
import datetime


def main(file_number = 10):
    col2 = connect('db','commentaire')
    #col2.drop() # à enlever ? 
    col = connect('db','id')
    id_list = get_id(col)
    line_to_process = col.count_documents({'status_commentaire':"0"})
    while line_to_process > 0:
        # access to a random data from the database (should limit functions that try to acess to the same value )
        elt = list(col.aggregate([{ "$sample": { "size": 1 } }]))[0]
        if elt["status_commentaire"] == "0":
            try : 
                # code to create a txt file with all the comments
                commande = "youtube-comment-downloader --youtubeid " +elt['id']+ " --output comments_"+str(file_number)+".txt"
                os.system(commande)

                # reading the txt file
                with open("comments_"+str(file_number)+".txt","r") as f:
                    a = f.readlines()
                for line in a : 
                    # convert the string to a json 
                    temp = json.loads(line)
                    # gather only the required information (comment id, the comment and the votes)
                    temp_dict = {"video_id":elt["id"], "comment_id" : temp["cid"],"texte" : temp["text"],"votes" : temp["votes"],"date": datetime.datetime.today().strftime('%Y/%m/%d')}
                    # inserting all the comments into the db 
                    store_data(col2,temp_dict)
                update_data(col,elt['id'],"status_commentaire","1") # say we only downloaded the video
                # if elt["status"]=="ongoing": # case there was no processing on this video
                #     update_data(col,elt['id'],"status","ongoing_commentaire") # say we only downloaded the video
                # elif elt['status'] == "ongoing_video" : # case comment where processed
                #     update_data(col,elt['id'],"status","done") # as we downloaded the video we put done here 
                line_to_process = col.count_documents({'status_commentaire':"0"})
            except : 
                update_data(col,elt['id'],"status_commentaire","2") # say we only downloaded the video 
    return 0

if __name__=="__main__": 
    main()