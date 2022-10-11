# Youtube-Explorer

Ce projet a été réalisé dans le cadre d'un projet à ESIEE Paris sous la supervison de Jean-François Bercher et Romain Negrel.  

Les membres du groupes sont : 
-  Raphaëlle JALLAT
-  Mélissa MEKKI DAOUADJI  
-  Vithulaksan NAGULESWARAN
-  Julien RAVINDRARASA
-  Haïtham SOUEF
-  Andres VILLARRAGA MORALES
## Pré requis
-  Avoir la version ```1.xx``` de docker-compose
-  Il faut dans un premier temps téléchager le fichier csv contenant les différents identifiants des vidéos Youtube. Il faut le nommer ```2021_10_08_video_ids.csv``` et le mettre dans le dossier ```scripts``` . 
-  Remplacer les chemins d'accès dans le fichier ```docker-compose-scripts.yml``` respectivement   
```/Path/to/youtube-explorer/image:/work/image``` (ligne 15)  
```/Path/to/youtube-explorer/video:/work/video```  (ligne 16).
- Il faut téléchager le dossier ```models``` qui contient les modèles des IA utilisés pour déterminer l'âge et le genre d'une personne. Ce dossier se trouve dans le google drive du projet, dans le dossier ```age-gen-rec```  (nos tuteurs y ont accès). Le dossier ```models``` doit se trouver à la racine du projet.
## Lancement du projet 

Après avoir réalisé les étapes précédentes, pour obtenir les premiers résultats il faut taper la commande:  
```docker-compose -f docker-compose-scripts.yml up --build```  
pour téléchager les vidéos et appliquer les différentes fonctions d'analyse sur le genre ou bien les placements de produits par exemple. 
Il faut ensuite taper la commande :  
```docker-compose -f docker-compose-interface.yml up --build```  
Cette commande lance le serveur pour avoir accès à l'interface. Pour pouvoir accèder à l'interface et y voir les données on doit taper l'adresse suivante dans un navigateur :  
```localhost:10000/```
