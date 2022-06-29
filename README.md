**Welcome to the BFM Anonymizer Realtime !**
This program will detect faces realtime on your webcam and blur them to anonymize.

## How to start
You need `python`, `OpenCV` and `skimage` to launch it :
```
pip install opencv-python
pip install scikit-image
```

Then you can start it from your desktop :
```
python main.py
```

To quit the program, use "q".

Pour le floutage, nous avons tout d'abord utilisé un flou gaussien. Plus le floutage était important plus la fluidité de la capture vidéo était diminuée. Nous avons donc en moyenne 10 FPS avec cette technique.
Nous sommes par la suite passés par la library openCV en effectuant un downscale puis un upscale de la résolution nous permettant d'avoir un effet de floutage pixelisé. Nous sommes en moyenne à 20 FPS.

Pour la détection, nous avions au départ une détection uniquement lorsqu'un visage était détecté. Cela posait donc un problème si la détection était interrompue ou indétecté ce qui laissait découvrir le visage.
Nous avons d'en un premier temps fait en sorte que si aucun visage était détecté alors le floutage de la dernière détection était affiché.
Le résultat était plutôt concluant, très performant, cependant, il ne fonctionnait pas en présence de différents visages.
Nous avons donc trouvé une autre alternative qui consiste à appliquer un timer sur chaque floutage