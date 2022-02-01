#from .downloader import main
import os
import sys


#liste des id des vidéos 
id_list = [
        'L-CYdL7NksA',
        'eiLo-Xqrc_w'
]

# nom de notre fichier json qui récupere les infos
test = 'test'
for i in id_list : 
    commande = "youtube-comment-downloader --youtubeid " + i + " --output " + test +".json"
    #print(commande)
    os.system(commande)
