from bs4 import BeautifulSoup
import urllib
import re, json 


def download_json(youtube_id):
    # Téléchargement du contenu HTML de la page
    response = urllib.request.urlopen('https://www.youtube.com/watch?v=' + youtube_id)
    htmlContent = response.read().decode('UTF-8')


    # Extraction du contenu de la variable ytInitialPlayerResponse
    soup = BeautifulSoup(htmlContent, "html.parser")
    pattern = re.compile(r"^var ytInitialPlayerResponse = (.*?);$", re.MULTILINE | re.DOTALL)
    script = soup.find("script", text=pattern)

    ytInitialPlayerResponse = json.loads(pattern.search(script.text).group(1))


    oRes = {}

    oRes['title']= ytInitialPlayerResponse['videoDetails']['title']
    oRes['video_duration']= int(ytInitialPlayerResponse['videoDetails']['lengthSeconds'])

    tmpParams = ytInitialPlayerResponse['storyboards']['playerStoryboardSpecRenderer']['spec'].split("|")

    base_url = tmpParams[0]
    tmpParams = tmpParams[1:]

    storyboards = []
    for i in range(len(tmpParams)):
        tmp_url = base_url.replace("$L", str(i))
        tmpSbInfo = tmpParams[i].split("#")
        sbInfo = {}
        sbInfo['sub_image_width'] = int(tmpSbInfo[0])
        sbInfo['sub_image_height'] = int(tmpSbInfo[1])
        sbInfo['nb_total_sub_image'] = int(tmpSbInfo[2])
        sbInfo['nb_col_by_image'] = int(tmpSbInfo[3])
        sbInfo['nb_row_by_image'] = int(tmpSbInfo[4])
        if int(tmpSbInfo[5]) == 0:
            sbInfo['time_in_between'] = (oRes['video_duration']*1000)//sbInfo['nb_total_sub_image']
        else:
            sbInfo['time_in_between'] = int(tmpSbInfo[5])
        image_file_name = tmpSbInfo[6]
        sigh = tmpSbInfo[7]
        
        tmp_url = tmp_url.replace("$N", image_file_name) + "&sigh=" + sigh

        images = []
        nb_image = 0
        nb_sub_images = 0
        while nb_image*(sbInfo['nb_col_by_image']*sbInfo['nb_row_by_image']) < sbInfo['nb_total_sub_image']:
            image = {}
            image['url'] = tmp_url.replace("$M", str(nb_image))
            sub_images = []
            for row in range(sbInfo['nb_row_by_image']):
                if(nb_sub_images > sbInfo['nb_total_sub_image']):
                    continue
                for col in range(sbInfo['nb_col_by_image']):
                    if(nb_sub_images > sbInfo['nb_total_sub_image']):
                        continue
                    sub_image = {}
                    sub_image['timecode'] = nb_sub_images*sbInfo['time_in_between']//1000
                    crop={}
                    crop['x_start'] = sbInfo['sub_image_width']*col
                    crop['x_end'] = sbInfo['sub_image_width']*(col + 1)
                    crop['y_start'] = sbInfo['sub_image_height']*row
                    crop['y_end'] = sbInfo['sub_image_height']*(row + 1)
                    sub_image['crop'] = crop
                    sub_images.append(sub_image)
                    nb_sub_images = nb_sub_images + 1
                    
            image['sub_images'] = sub_images
            images.append(image)
            nb_image = nb_image + 1
        sbInfo['images'] = images
        storyboards.append(sbInfo)
        
    oRes['storyboards'] = storyboards
    return oRes

def download_vignette(oRes):
    file_name = oRes["title"]
    count = 0 
    for elt in oRes['storyboards'][2]['images']:
        urllib.request.urlretrieve(elt['url'],"image/"+file_name+"-"+str(count)+".png")
        count +=1
    