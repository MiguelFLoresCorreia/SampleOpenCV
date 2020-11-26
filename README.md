# WebCam Mix - Mixez avec votre webcam

## Projet réalisé par :
- Cussac Théo
- Camagny Robin
- Flores Correia Miguel

## SUJET :

Lancer des samples par rapport aux mouvements des mains captés par la caméra.

## CHOIX TECHNIQUES :

- Python
	On utilise python avec lequel on utilisera les bibliothèques numpy, opencv (pour la capture caméra et sa manipulation) et pygame (pour manipuler la playlist de musique) 

- OpenCV
	Open source et bien documenté

- Pygame
	Outil simple d'utilisation pour géré notre piste musicale

## EXPLICATION RAPIDE DE LA METHODE DE FONCTIONNEMENT :

Des zones de detection seront préalablement placé au bord de la caméra, à chaques mouvements détectés dans cette case, un sample de musique sera lancé en continue jusqu'à ce qu'un mouvement est redétecté dans cette même case. Il est possible de lancer plusieurs samples en même temps.

## UTILISATION :

### Prérequis :

- Caméra branchée à votre ordinateur
- Python 3 installer 
- Bibliothèques nécessaire à installer : 
	- numpy (pip install numpy)
	- pygame (pip install pygame)
	- opencv (pip install opencv-python)

### Installation et lancement :

- Clone du git (git clone https://github.com/MiguelFLoresCorreia/SampleOpenCV.git)

- Lancer le programme (python webCamMix.py)

- Tuto vidéo : 

### Explication du code :

Dans un premier temps le code nous demande de choisir le dossiers contenant les notes ou les samples (les 10 premiers samples dans le document). Une fois cela fait le code va calculer selon le nombre de notes ou samples la taille des carrés. On associe alors chaque note/sample à un carré.
La caméra va capturer une succession d'images dont la précédente va être comparée à la nouvelle. Si un mouvement est détecté au niveau d'un carré cela va actionner sa musique attribuée.
Le son dura 0.5 secondes en mode piano ou jusqu'à son arrêt par l'utilisateur en mode infini.
Pour changer le mode il faut appuyer sur la touche 'p' et pour quitter la touche 'q' qui va nous faire sortir de la boucle et arrêter le programme.
