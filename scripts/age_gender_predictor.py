import cv2
import os
import torch
from os.path import join
from facenet_pytorch import MTCNN, InceptionResnetV1
from operator import itemgetter, attrgetter
import matplotlib.pyplot as plt
from skimage import io

class AgeGenderPredictor:


    def __init__(self, genderModel, ageModel):
        # load gender model
        if(len(genderModel)!=3 or len(genderModel)!=3):
            raise Exception('genderModel and ageModel must contain 3 elements')
        self.gender_model_path = genderModel[0]
        self.gender_caffemodel = genderModel[1]
        self.gender_prototxt = genderModel[2]
        self.gender_model = self.load_model(self.gender_model_path, self.gender_caffemodel, self.gender_prototxt)

        # load age model
        self.age_model_path = ageModel[0]
        self.age_caffemodel = ageModel[1]
        self.age_prototxt = ageModel[2]
        self.age_model = self.load_model(self.age_model_path, self.age_caffemodel, self.age_prototxt)
        self.device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    def load_model(self, model_path, caffemodel, prototxt):
        caffemodel_path = join(model_path, caffemodel)
        prototxt_path = join(model_path, prototxt)
        model = cv2.dnn.readNet(prototxt_path, caffemodel_path)
        return model


    def predict(self, model, img, height, width):
        face_blob = cv2.dnn.blobFromImage(img, 1.0, (height, width), (0.485, 0.456, 0.406))
        model.setInput(face_blob)
        predictions = model.forward()
        class_num = predictions[0].argmax()
        confidence = predictions[0][class_num]
        return class_num, confidence

    def processResults(self, genderArray, ageArray):
        manProb=0
        womanProb=0
        childProb=0
        youngprob=0
        adultProb=0
        oldProb=0
        for gender,prob in genderArray:
            if gender ==1:
                manProb=manProb+prob
            else:
                womanProb=womanProb+prob
        gender= 'man' if manProb > womanProb else 'woman'
        for age,prob in ageArray:
            #age= age-5 if gender=='man' else age
            age=0 if len(ageArray)>1 and prob < 0.1  else age
            childProb= childProb+prob if age<15 else childProb
            youngprob= youngprob+prob if age>=15 and age < 25 else youngprob
            adultProb= youngprob+prob if age>=25 and age < 65 else adultProb
            oldProb= youngprob+prob if age>=65 else oldProb
        ageArray=[{'label':'child','key':childProb},{'label':'young','key':youngprob},{'label':'adult','key':adultProb},{'label':'old','key':oldProb}]
        ageArray=sorted(ageArray, key=itemgetter('key'), reverse=True)
        return gender,ageArray[0]['label']
        

    def gender_age_reco(self, subImg, mtcnn, checkFirstFace):
        faces, _ = mtcnn.detect(subImg)
        h, w = [224,224]
        if(checkFirstFace):
            faces=[faces[0]]
        descImg=''
        if faces is not None:
            cont=0
            faces[0]
            frame_rgb = cv2.cvtColor(subImg, cv2.COLOR_BGR2RGB)
            for (x1, y1, x2, y2) in faces:
                left = int(0.6 * x1)     # + 40% margin
                top = int(0.6 * y1)       # + 40% margin
                right = int(1.4 * x2)   # + 40% margin
                bottom = int(1.4 * y2) # + 40% margin
                face_segm = frame_rgb[top:bottom, left:right]
                if face_segm.shape[0] > 0 and face_segm.shape[1] > 0: 
                    gender, gender_confidence = self.predict(self.gender_model, face_segm, h, w)
                    age, age_confidence = self.predict(self.age_model, face_segm, h, w)
                    ageResult= [age-5, age_confidence]
                    genderResult = [gender,gender_confidence]
                    gender = 'man' if gender == 1 else 'woman'
        return genderResult,ageResult



    def get_people_age_gender(self, imgs_dir):
        container= os.listdir(imgs_dir)
        results=[]
        for directory in container:
            if os.path.isdir(os.path.join(imgs_dir, directory)):
                with os.scandir(os.path.join(imgs_dir, directory)) as images:
                    img_folder=os.path.join(imgs_dir, directory)
                    arrayAge=[]
                    arrayGender=[]
                    for img in images:
                        mtcnn = MTCNN(keep_all=False, device=self.device)
                        image=io.imread(os.path.join(img_folder,img.name))
                        gRes, ageRes = self.gender_age_reco(image, mtcnn, True)
                        arrayAge.append(ageRes)
                        arrayGender.append(gRes)
                    results.append(self.processResults(arrayGender,arrayAge))
        return results
