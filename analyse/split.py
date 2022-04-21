import ffmpeg
import cv2
import numpy as np



def spliter(filename,fps_x):
    (
        ffmpeg
        .input(filename)
        .filter('fps', fps=fps_x)
        .output('test-%d.png', start_number=0)
        .overwrite_output()
        .run()
    )


def concat(img_number,video_name, folder = ""):
    #nombre de photos par vidéo

    #Lecture des images
    reader = [cv2.imread(video_name+str(k)+'.jpg') for k in range(img_number) ]
    #on assemble en pack de 29 les photos horizontalement
    cutter = lambda liste, size: [liste[i:i+size] for i in range(0, len(liste), size)]
    #On coupe tout les 29
    reader_splited = cutter(reader,29)
    #Conctenation of the image
    d = [cv2.hconcat(element) for element in reader_splited]
    x = cv2.vconcat(d[0:28])
    cv2.imwrite(video_name+'.jpg', x)


def samesize(pictures):
    return 0


# nombres d'images par secondes
#fps_x = 1 : 1 une impage par seconde
#fps_x = 1/60 : 1 image toutes les minutes
#fps_x = 1/600 : 1 image toutes les 10 minutes


def find_just_fps(filename):
    #récuperer le temps de la video
    probe = ffmpeg.probe(filename)
    time = float(probe['streams'][0]['duration'])
    #
    fps = 100.0/float(time)#840
    return  fps

