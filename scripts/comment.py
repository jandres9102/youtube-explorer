import os, json 
from database import *
import datetime


def main():
    col2 = connect('db','commentaire')
    col2.drop()
    col = connect('db','id')
    id_list = get_id(col)
    result_list = [] # list to see the result
    for elt in id_list:
        # code to create a txt file with all the comments
        commande = "youtube-comment-downloader --youtubeid " +elt['id']+ " --output comments.txt"
        os.system(commande)

        # readin the txt file
        with open("comments.txt","r") as f:
            a = f.readlines()
        for line in a : 
            # convert the string to a json 
            temp = json.loads(line)
            # gather only the required information (comment id, the comment and the votes)
            temp_dict = {"comment_id" : temp["cid"],"texte" : temp["text"],"votes" : temp["votes"],"date": datetime.datetime.today().strftime('%Y/%m/%d')}
            # inserting all the comments into the db 
            store_data(col2,temp_dict)
            
    return 0

if __name__=="__main__": 
    main()
    

