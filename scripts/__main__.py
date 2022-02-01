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
    commande = "python downloader.py --youtubeid " + i + " --output " + test +".json"
    #print(commande)
    os.system(commande)

#if __name__ == '__main__':

   # main()c