from multiprocessing import Process # import to parallize comment and video download 
import people_counter as counter
import face_recognition as fr
import age_gender_predictor as age


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
