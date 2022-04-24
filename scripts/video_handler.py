import cv2
import os
import ffmpeg

class VideoHandler:


    def __init__(self, videoPath, imagesFolder):
        
        self.video_path = videoPath
        if not os.path.isdir(imagesFolder):
            os.mkdir(imagesFolder)
        self.images_folder= imagesFolder


    def spliter(self,filename,fps_x):
        (
            ffmpeg
            .input(filename)
            .filter('fps', fps=fps_x)
            .output(self.images_folder+'/'+filename+'%d.jpg', start_number=0)
            .overwrite_output()
            .run()
        )


    def find_just_fps(self,filename):
        #récuperer le temps de la video
        probe = ffmpeg.probe(filename)
        time = float(probe['streams'][0]['duration'])
        #
        fps = 25.0/float(time)#840
        return  fps

    def get_video_images(self):
        fps_x = self.find_just_fps(self.video_path)
        self.spliter(self.video_path,fps_x)
