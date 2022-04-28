from skimage import io 
import os
from database import *

from downloader import * 


def crop_image(oRes,image_path="image/"):
    """
        function to crop image, the output is a list of image (np.array)
    """
    file_name = oRes["title"]
    output_image = []
    # lecture de la grande image
    list_images = os.listdir(image_path)
    list_image = [ elt for elt in list_images if file_name in elt]
    for image in list_image:
        image = io.imread(image_path+image)
        for sub_image in oRes['storyboards'][2]['images'][-2]['sub_images']:
            crop = sub_image['crop']
            img = image[crop['y_start']:crop['y_end'], crop['x_start']:crop['x_end'],:]
            output_image.append(img)
    return output_image

def get_timecode(youtube_id):
    """
        Function that take the youtube id to get the oRes object and get the time when image where taken from oRes
    """
    col_meta = connect('db','meta')
    oRes = col_meta.find_one({"id":youtube_id})
    timecode = []
    for vignette in oRes['storyboards'][0]["images"] : 
        for sub_image in vignette["sub_images"]:
            timecode.append(sub_image["timecode"])
    return timecode

if __name__ == "__main__":
    yt_vid_id = "ZVYaGfs80b0"
    oRes = download_json(yt_vid_id)
    download_vignette(oRes)
    image = crop_image(oRes,)
