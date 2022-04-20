import comment as c # import function to download comments
import script as sc # import function to download meta-data
from age_gender_predictor import AgeGenderPredictor
from video_handler import VideoHandler
from face_recognition_processor import FaceRecognitionProcessor
from multiprocessing import Process # import to parallize comment and video download 

def main(file_value = 10):
	c.main(file_value) #function to  download comment
	sc.main() #function to download meta-data 
	#print('dd')

if __name__ == "__main__" :
	processor = [] # list that will contain all of our 8 process 
	for k in range(1,9):
		if k%2==0 : 
			p = Process(target=sc.main,args=())   
		else : 
			p = Process(target=c.main,args=(k,))   
		processor.append(p) # add this process to the list 
		p.start() # start of the process 
	for elt in processor:
		elt.join() # to end all processes
	videoHandler= VideoHandler('ab.mp4','video-images')
	videoHandler.get_video_images()
	faceRecognition=FaceRecognitionProcessor('video-images','faces-images')
	faceRecognition.get_picture_faces('jpg')
	#"""
	#location of the NN models related to age-gender recognition
	genderModel=['models/gender','gender.caffemodel','gender.prototxt']
	ageModel=['models/age','dex_chalearn_iccv2015.caffemodel','age.prototxt']
	#declaring an object to charge these models
	aGenPred= AgeGenderPredictor(genderModel,ageModel)
	#the input parameter is where the images to apply the NN are located
	print(aGenPred.get_people_age_gender('./images/'))
	#"""