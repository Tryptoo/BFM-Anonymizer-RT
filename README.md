**Welcome to the BFM Anonymizer Realtime !**
This program will detect faces realtime on your webcam and blur them to anonymize.

It has been made by Nicolas Perot, Loïck Roberjot and Ulysse Regnier for the "Analyse des images" course in CNAM-ENJMIN.

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

## Parameters
Some variables you can change to optimize or change the final result in the `constants.py` file.

### Face Detection

#### MIN/MAX_RECT_SIZE
Change the min and max detection of the face. Can optimize framerate but can also miss some small or big faces.

#### FACE_RECOGNITION_DISTANCE
Check between two frames if a face is close enough to another to be consider the same face. If yes, it will move it's blur rect, if not it will create a new blur.

You should use a smaller distance for smaller faces.

#### RECT_DELETE_DELAY
Delete a blur after this time (in sec). This cooldown is a workaround of some leak in the face detection.

#### FACE_RECT_INCREASE_RATIO
A simple multiplier on the face rect to make sure all the face is blurred.

#### FACE_RECT_OFFSET
A simple offset on the face rect to make sure all the face is blurred.

### Blur

#### BLUR_FACTOR
**Only for gaussian blur**. Intensity of gaussian blur. Can affect framerate.

#### BLUR_UPDATE_DELAY
Cooldown on the blur. If equals 0, the blur will be calculated every frame. If higher, the blured face will stay the same until the next blur calculation. This affects framerate but can cause some crash and weird face shaking.

#### BLUR_WITH_CV2
`False` : Gaussian blur

`True` : Downscale then upscale on opencv

The openCV solution is much better for framerate.

### What you should do

To save framerate, miss crash and have a decent detection, we advise you not to change parameters.

You can adapt the `FACE_RECOGNITION_DISTANCE` and `MIN/MAX_FACE_RECT_SIZE` to your scene. It will depend on the size of the faces on the image.

You should always have a good light and less shadows on your faces.

If you want to use gaussian blur, you should increase the `BLUR_UPDATE_DELAY` to something like 0.2 to have decent framerate.

## Analyse des images

### Détection des visages
La détection est souvent un peu frétillante et loupe parfois sur quelques frames. Cela pouvait donc parfois laisser le visage apparaître et provoquer certains tremblements.

Nous avons donc priorisé l'anonymisation et empêché que les visages ne soient pas floutés en ajoutant un cooldown pour chaque visage. Si un visage n'est plus détecté, le précédent flou reste pendant un certain temps. Cette solution permet d'empêcher la majorité des sautes de détections.

La lumière est aussi un soucis majeur de la détection. Pour cela nous avons tenté différents traitements sur l'image tel qu'une amélioration de la netteté par niveaux de gris. Cependant, les résultats n'ont pas été concluants. Après différentes observation, la configuration idéale est une salle bien éclairée et des visages avec le moins d'ombre possible.

### Solution de floutage
Pour le floutage, nous avons tout d'abord utilisé un flou gaussien, comme nous l'avions vu en cours. Plus le floutage était important plus la fluidité de la capture vidéo était diminuée. Nous avons donc en moyenne à 5 FPS avec cette technique.

Afin d'augmenter le framerate, nous avons tout d'abord procédé à un cooldown paramétrable sur le floutage. Cela permet de flouter l'image moins souvent par seconde et gagner en performance. Cependant, entre les floutages, la même image du visage flouté est gardé en attendant le prochain flou, ce qui peut donner une sensation de tremblement du visage (puisque la detection tremble mais l'image ne change pas), et on peut remarquer assez facilement que l'image ne change pas pendant un certain temps. Cette solution provoque aussi des crashs que l'on a pas eu le temps de corriger lorsqu'un visage sort de l'écran.

Nous sommes par la suite passés par la library openCV en effectuant un downscale puis un upscale de la résolution nous permettant d'avoir un effet de floutage pixelisé. Nous avons réussi à atteindre les 14 fps, en désactivant la solution précédente de cooldown du flou (un flou / frame / visage).