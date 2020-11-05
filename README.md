# SampleOpenCV

NOM :

SampleOpenCV

PARTICIPANTS :

Cussac Théo
Camagny Robin
Flores Correia Miguel

SUJET :

Lancer des samples par rapport aux mouvements des mains captés par la caméra.


CHOIX TECHNIQUES :

Camera de l'ordinateur, librairie OpenCV, des fichiers audios.

OpenCV est très bien documenté et est open source.

EXPLICATION RAPIDE DE LA METHODE DE FONCTIONNEMENT :

Des carrées de detection seront préalablement placé à certains bords de la caméra, à chaque mouvement détecté dans cette case, un sample sera lancé en continue jusqu'à ce qu'un mouvement est redétecté dans cette même case. Il sera donc possible de lancer plusieurs samples en même temps.