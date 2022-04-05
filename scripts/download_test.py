from __future__ import unicode_literals
import youtube_dl 

ydl_opts = {'outtmpl': './video/%(title)s.%(ext)s'}

with youtube_dl.YoutubeDL(ydl_opts) as ydl : 
    meta = ydl.extract_info('https://www.youtube.com/watch?v=maXnoLa1UOs',download=True)

# for key in meta.keys():
#     print(f"pour la clé {key} oa l'information {meta[key]}")

print(meta)