# Youtube 

## Pour lancer le projet 
-  Il faut cloner ce repository 
```git clone https://github.com/jandres9102/youtube-explorer ```   
-  Lancer la commande ```docker-compose build``` et ```docker-compose up```  

### note 
Par défaut on ne télécharge pas les vidéos (pour le faire faut remplacer le False des lignes 32 pour ```script.py``` de la branche main et la ligne XX pour ```script.py``` de la branche thread )
Il y a un niveau de l'option ``` ydl_opts = {'outtmpl': './downloadedsongs/%(title)s.%(ext)s'}  ``` le chemin où les vidéos vont se téléchager. Remplacer ça par le chemin pour accèder au NAS.
La version du programme se trouvant sur la branche ```main``` fonctionne sans thread.  
Il y a une version qui fonctionne avec du multiprocessing dans la branch thread (mais on n'a pas vraiment l'impression que c'est plus rapide)
