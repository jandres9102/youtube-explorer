import people_counter as counter
import face_recognition_processor as fr
import age_gender_predictor as age
import video_handler as video
from database import *
import shutil, os
import pwd


# videoHandler= VideoHandler('dummy.mp4','video-images')
	# videoHandler.get_video_images()
	# faceRecognition=FaceRecognitionProcessor('video-images','faces-images') # dans faces images il y a uniquement les visaages détéectées même des doubblons 
	# faceRecognition.get_picture_faces('jpg')
	# #"""
	# #location of the NN models related to age-gender recognition
	# genderModel=['models/gender','gender.caffemodel','gender.prototxt']
	# ageModel=['models/age','dex_chalearn_iccv2015.caffemodel','age.prototxt']
	# #declaring an object to charge these models
	# aGenPred= AgeGenderPredictor(genderModel,ageModel)
	# #the input parameter is where the images to apply the NN are located
	# print(aGenPred.get_people_age_gender('scripts/images/'))
	#"""

def main(file_number = 10):
    """
        Main function 
        Return nothing. => Will read description and return the domain 
        name in video then increase the number of time the link was in a youtube description
    """
    # print("Dans la fonction deep analyse")
    col_analyse = connect('db','analyse')
    col_id = connect('db','id')
    col_meta = connect('db','meta')
    col_link = connect('db','link')
    count = 0

    line_to_process = col_id.count_documents({"status_image":"0"})
    with os.scandir('./video') as videos:
        for vid in videos:
            if vid.name != '.DS_Store': 
                video_id = vid.name.split(".")[0]
                # print("print video : "+video_id)
                elt_meta = list(col_meta.find({"id":video_id})) # elt est un objet qui contient les infos de la collection id
                if len(elt_meta)==0:
                    elt_meta =list(col_meta.find({"title":video_id}))
                # print(elt_meta)
                # print(elt_meta[0]["id"])
                elt = list(col_id.find({"id":elt_meta[0]["id"]}))[0]
                # print(elt)
                update_data(col_id,elt["id"],"status_image","1")
                if elt["status_video"]=="1" and elt["status_image"]=="0":  # case where we downloaded meta data about the video but didn't processed image to determin gender
                    video_name = elt["id"]
                    os.mkdir('./processor-img')
                    user= pwd.getpwuid(os.getuid())[0]
                    os.system('chown '+user+" ./video/"+vid.name)
                    videoHandler = video.VideoHandler("./video/"+vid.name,'./processor-img/video')
                    videoHandler.get_video_images()

                    faceRecognition = fr.FaceRecognitionProcessor('./processor-img/video','./processor-img/faces')
                    faceRecognition.get_picture_faces('jpg')

                    L = counter.loader('./processor-img/faces')
                    L = counter.encodeur(L)
                    ALPHA = counter.counter(L)
                    index_vis = ALPHA[1]
                    counter.save(index_vis,'./processor-img/faces','./processor-img/people')
                    # print(os.listdir("./processor-img/people"))
                    genderModel=['models/gender','gender.caffemodel','gender.prototxt']
                    ageModel=['models/age','dex_chalearn_iccv2015.caffemodel','age.prototxt']
                    #declaring an object to charge these models
                    aGenPred= age.AgeGenderPredictor(genderModel,ageModel)
                    # print(aGenPred.get_people_age_gender('./processor-img/people'))
                    
                    update_data(col_analyse,elt["id"],"gender",aGenPred.get_people_age_gender('./processor-img/people'))
                    shutil.rmtree('processor-img')
            else : 
                pass
    #shutil.rmtree('video')


if __name__ == "__main__":
    main()