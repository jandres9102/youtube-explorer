import os, json 
import cv2 as cv

class FaceDetection:
    def __init__(self):
        self.cv_dir= os.path.dirname(os.path.abspath(cv.__file__))
        print(self.cv_dir)
    def detecting(self,img_path):
        orig_image=cv.imread(img_path)
        #Convert color image to grayscale for Viola-Jones
        grayscale_image = cv.cvtColor(orig_image, cv.COLOR_BGR2GRAY)
        # Load the classifier and create a cascade object for face detection
        face_cascade = cv.CascadeClassifier(self.cv_dir+'/data/haarcascade_frontalface_alt.xml')
        detected_faces = face_cascade.detectMultiScale(grayscale_image)
        for (column, row, width, height) in detected_faces:
            cv.rectangle(
                orig_image,
                (column, row),
                (column + width, row + height),
                (0, 255, 0),
                2
            )
        cv.imshow('Image', orig_image)
        cv.waitKey(0)
        cv.destroyAllWindows()




def main():
    fd=FaceDetection()
    fd.detecting('test_img.jpg')

if __name__ == "__main__" :
    main()
