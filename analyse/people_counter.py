import dlib
import face_recognition
from PIL import Image
import numpy as np
import os
from skimage import io
import matplotlib.pyplot as plt
import urllib
from bs4 import BeautifulSoup
import re
import json
import matplotlib.image as mpimg
import random




MARGIN = 0.7

#On charge toutes les images     
def loader(name_folder):
    loaded_images = []
    image_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir(name_folder+'/'))
    paths_to_images = [name_folder+'/' + x for x in image_filenames]
    for image in paths_to_images:
        d = face_recognition.load_image_file(image)
        loaded_images.append(d)
    return loaded_images    

#On encode toutes les images qui ont été chargé au préalable     
def encodeur(loaded_images):
    vis_encoder = []
    for image in loaded_images:
        d = face_recognition.face_encodings(image,model = 'cnn')
        if d == []:
            next
        else:
            d = d[0]
            vis_encoder.append(d)
    return vis_encoder

#On lui donne une liste d'image encoder et il retourne le nombre de personne

def counter(set_photo, margin = MARGIN):
    l = []
    ind = [k for k in range(len(set_photo))]
    L = []
    while len(set_photo)>0:
        lp = []
        lind = []
        lp.append(set_photo.pop(0))
        lind.append(ind.pop(0))
        k = 0
        while k<len(set_photo):
            if face_recognition.face_distance(lp, set_photo[k])[0]<margin:
                lind.append(ind[k])
                lp.append(set_photo[k])
                set_photo.pop(k)
                ind.pop(k)
            else :
                k = k+1
        L.append(lind)
        l.append(lp)
    return len(l),L
    
 
def save(index_vis, name_folder,people_folder):
    image_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir(name_folder+'/'))
    paths_to_images = [name_folder+'/' + x for x in image_filenames]
    os.system('mkdir ' +people_folder)
    for k in range(len(index_vis)):
        os.system('mkdir ' +people_folder+'/dir_per-'+str(k))
        for val in index_vis[k]:
            int = val
            img = paths_to_images[int]
            img = Image.open(img)
            img.save(people_folder+'/dir_per-'+str(k)+'/'+str(int)+'.jpg')
            plt.figure()
            plt.title(people_folder+'/dir_per-'+str(k)+'/'+str(int)+'.jpg')
            plt.imshow(img)