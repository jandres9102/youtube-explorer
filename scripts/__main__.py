#from .downloader import main
import os
import sys


#id = 'L-CYdL7NksA' 
id_list = [
        'L-CYdL7NksA',
        'eiLo-Xqrc_w'
]

test = 'test'
for i in id_list : 
    commande = "youtube-comment-downloader --youtubeid " + i + " --output " + test +".json"
    #print(commande)
    os.system(commande)
