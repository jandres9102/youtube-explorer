import os, json 
from database import *

def main():
    id_list = get_id()
    result_list = [] # list to see the result
    for elt in id_list:
        # code to create a txt file with all the comments
        commande = "youtube-comment-downloader --youtubeid " +elt+ " --output comments.txt"
        os.system(commande)

        # readin the txt file
        with open("comments.txt","r") as f:
            a = f.readlines()
        for line in a : 
            # convert the string to a json 
            temp = json.loads(line)
            # gather only the required information (comment id, the comment and the votes)
            temp_dict = {"comment_id" : temp["cid"],"texte" : temp["text"],"votes" : temp["votes"]}
            # code to insert this json to the mongodatabase
            result_list.append(temp_dict) # temporary 
    return result_list

if __name__=="__main__": 
    main()
