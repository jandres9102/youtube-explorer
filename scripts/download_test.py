from __future__ import unicode_literals
import youtube_dl 
import os
ydl_opts = {'outtmpl': './video/%(title)s.%(ext)s'}

with youtube_dl.YoutubeDL(ydl_opts) as ydl : 
    meta = ydl.extract_info('https://www.youtube.com/watch?v=4MCWoA-_dIg',download=False)

for key in meta.keys():
    # print(f"pour la clé {key} oa l'information {meta[key]}")
    print(f"On a les clé suivante {key}")

print(meta["description"])
print(meta["tags"])
print(meta["ext"])

commande = 'curl -s https://www.youtube.com/watch?v=9lnh--ZOPyo | grep "paidContentOverlayRenderer" >> result.txt'
os.system(commande)
print(os.stat("result.txt").st_size == 0)
# print(meta)