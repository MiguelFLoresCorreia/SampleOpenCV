# SampleOpenCV

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

- Lancer le programme (py detecteur.py)


video demo/ pouvoir mettre ses propres samples