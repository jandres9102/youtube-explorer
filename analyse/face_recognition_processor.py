import cv2
import os
import ffmpeg
import face_recognition
from PIL import Image

class FaceRecognitionProcessor:


    def __init__(self, imagesFolder, facesFolder):
        self.images_folder = imagesFolder
        if not os.path.isdir(facesFolder):
            os.mkdir(facesFolder)
            os.chmod(facesFolder, 436)
        self.faces_folder= facesFolder


    def get_picture_faces(self, typeof_picture):
        image_filenames = filter(lambda x: x.endswith(typeof_picture), os.listdir(self.images_folder+'/'))
        paths_to_images = [self.images_folder+'/' + x for x in image_filenames]
        count=0
        all_faces=self.faces_folder+'/test_'
        for element in paths_to_images:
            image = face_recognition.load_image_file(element)
            # See also: find_faces_in_picture_cnn.py
            face_locations = face_recognition.face_locations(image)
            for face_location in face_locations:
                top, right, bottom, left = face_location
                # You can access the actual face itself like this:
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                pil_image.save(all_faces+str(count)+'.jpg')
                count=count+1
