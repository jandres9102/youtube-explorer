import os, json 
from database import *



# .find({},{"id":1,""})

db, col2 = connect('db','commentaire')

def main():
    db,col = connect('db','id')
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
            temp_dict = {"comment_id" : temp["cid"],"texte" : temp["text"],"votes" : temp["votes"]}
            #
            store_data(col2,temp_dict)
            # code to insert this json to the mongodatabase
            result_list.append(temp_dict) # temporary 
    return result_list

if __name__=="__main__": 
    main()
    print(list(col2.find()))

