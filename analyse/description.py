import re,os 
import urllib.request, urllib.parse

from database import * 

# col = connect('db','meta')
# meta = get_oRes(col)
# for elt in meta : 
#     print(elt['description'])

description ="""Ceci est une description test avec l'url https://www.youtube.com/watch?v=
https://www.google.com/ 
http://tidd.ly/502e1408
https://www.naturaforce.com/
https://www.cyberghostvpn.com/
https://www.google.com
"""

description_marvel = """
Code marvel sur Natura force : https://www.naturaforce.com/

Twitch : https://www.twitch.tv/horcruxe9

T-shirt : https://mutant-shop.creator-spring.com/

Dlive : https://dlive.tv/Marvelfit?ref=marvelfit

Instagram : https://www.instagram.com/marvel.fitn...

Twitter : https://twitter.com/Marvel_Fit

Facebook : https://www.facebook.com/marvel.fit
"""

description_megan = """
Cliquez sur ce lien pour en découvrir plus su CyberGhost et leur INCROYABLE promotion juste pour vous : https://www.cyberghostvpn.com/MeganMorgan

On se retrouve aujourd'hui pour découvrir ensemble l'affaire de la famille Abaroa. Connaissiez vous cette affaire ? Qu'en avez vous pensé ? Laissez moi vos avis et opinions en commentaire.
Désolée pour le bug au début de la vidéo au niveau des images qui manquent…

On se retrouve bientôt dans de nouvelles vidéos 🖤
"""

description_manga = """
Vidéo roue libre où Billy et Amine suivent le camp d'entrainement pendant 10jours !

Réduction -40% MyProtein ►
http://tidd.ly/502e1408  code "MANGA"

Chaine de Rebeudeter : https://www.youtube.com/c/RebeuDeter
Chaine de Aminematue : https://www.youtube.com/c/Aminematue
Chaine de Inoxtag : https://www.youtube.com/channel/UCL9aTJb0ur4sovxcppAopEw

Discord MW pour s'entrainer et s'entraider à plusieurs : https://discord.gg/6QTtGZtRxn
Instagram : https://www.instagram.com/mangaworkout/
Twitter : https://twitter.com/MangaWorkout
"""





def create_url(sep_url):
    """
        Function that take a tuple and return an url 
    """
    url = ""
    if len(re.findall("(http|ftp|https)",sep_url[0])) > 0 :
        url = sep_url[0]+"://"
    for elt in sep_url[1:]:
        url += elt
    return url

def get_domain(list_url, social_link=["discord","snapchat","instagram","twitch.tv","facebook","youtube","twitter.com","t.me"]):
    """
        Function that takes a full url and return a domain name 
    """
    clean_url = []
    for url in list_url:
        domain = urllib.parse.urlparse(create_url(url)).netloc
        clean_url.append(domain)
    clean_url = list(set(clean_url))
    for link in social_link: 
        for url in clean_url:
            if link in url : 
                clean_url.remove(url)
                break 
    return clean_url


def get_raw_url(description):
    """
        Function to get all links available in a youtube video description
        Take a description and return a list of link
    """
    # regex that will be used to look for url link with http|https with :// or just www 
    urls_regex = "(http|ftp|https|):?\/?\/?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
    # list of all urls we find in the description there could be tiny link 
    urls= re.findall(urls_regex,description)
    full_url = [] # list that will contain all domain names
    # checking if link is a tiny link 
    for link in urls :
        link = create_url(link)
        try : 
            resp = urllib.request.urlopen(link)
            if resp.getcode() == 200:
                resp.url
                regex_url = re.findall(urls_regex,str(resp.url))[0]

                # case where there is a https or http in the link 
                if len(re.findall("(http|ftp|https)",regex_url[0])) > 0 :
                    # print("Depuis le if",regex_url)
                    full_url.append(regex_url) 
                else : 
                    full_url.append(re.findall(urls_regex,resp.url))
        except urllib.error.HTTPError :
            pass 
    return full_url

def isSponso(youtube_id,file_num=10):
    """
        Function that request the youtube page to check if there is a sponsorship in the video
    """
    if os.path.isfile("result"+str(file_num)+".txt"):
        os.remove("result"+str(file_num)+".txt")
    commande = 'curl -s https://www.youtube.com/watch?v='+youtube_id+'| grep "paidContentOverlayRenderer" >> result'+str(file_num)+'.txt'
    os.system(commande)
    if os.stat("result"+str(file_num)+".txt").st_size == 0 :
        return False
    os.remove("result"+str(file_num)+".txt")
    return True

def main(file_num = 10):
    """
        Main function 
        Return nothing. => Will read description and return the domain 
        name in video then increase the number of time the link was in a youtube description
    """
    col_analyse = connect('db','analyse')
    col_id = connect('db','id')
    col_meta = connect('db','meta')
    col_link = connect('db','link')
    count = 0
    # count the number of video to process 
    line_to_process = col_id.count_documents({'status_description':"0"})
    while line_to_process > 0:
        elt = list(col_id.aggregate([{ "$sample": { "size": 1 } }]))[0] # elt est un objet qui contient les infos de la collection id
        analyse = col_analyse.find_one({"id":elt["id"]}) # objet qui contient les infos dans la collection analyse pour la vidéo d'id 
        if elt["status_video"]=="1" and elt["status_description"]=="0":  # case where we downloaded meta data about the video
            description = col_meta.find_one({"id":elt["id"]})["description"]
            raw_url = get_raw_url(description) 
            clean_domain = get_domain(raw_url)
            update_data(col_id,elt["id"],"status_description","1") # says that we parsed this video description
            if isSponso(elt["id"],file_num):
                update_data(col_analyse,elt["id"],"isSponso","vidéo sponsorisée") 
            elif not isSponso(elt["id"],file_num) and len(clean_domain)>0 : 
                update_data(col_analyse,elt["id"],"isSponso","possible partenariat long terme") 
            else : 
                update_data(col_analyse,elt["id"],"isSponso","non") 

            if len(clean_domain) > 0:
                count = 0 
                for link in clean_domain : 
                    record = col_link.find_one({"link":link})
                    print(record)
                    if record is not None: 
                        count = record["count"]
                    update_data(col_link,link,"count",count+1) # add one to the number of time we saw this link
                update_data(col_analyse,elt["id"],"links",clean_domain)
        elif elt["status_video"]=="2": 
            update_data(col_id,elt["id"],"status_description","2") # erreur while trying to parse descriptin 
        line_to_process = col_id.count_documents({'status_description':"0"})
        

"""
1342347;y42PUGAZfXs
1342347;3bg8lhb1-wo
1342347;fjxJU4nMEDA
"""
# col_id = connect('db','id')
# col_meta = connect('db','meta')
# col_link = connect('db','link')
# ids = ["tAyev18kwc0","y42PUGAZfXs","3bg8lhb1-wo","fjxJU4nMEDA","es7wgBIZg6E"]

# for idx in ids: 
#     video_dic = {"id":idx,"status_video":"1","status_commentaire":"0","label":0,"status_description":"0","status_image":"0"}
#     col_id.insert_one(video_dic)
if __name__=='__main__':
    main()
# raw_url = get_raw_url(description_manga)
# domain = get_domain(raw_url)
# print(raw_url)
# print(domain)


