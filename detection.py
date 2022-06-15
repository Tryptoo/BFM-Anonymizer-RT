import skimage
import matplotlib.pyplot as plt
from skimage import io
from skimage.feature import Cascade
from skimage import data, exposure
from matplotlib import patches

# Charge le fichier contenant le modèle préentraîné
trained = skimage.data.lbp_frontal_face_cascade_filename()

# Détecteur
detector = Cascade(trained)

image = "Remplir par l'image"

detected = detector.detect_multi_scale(image,scale_factor=1.2,
                                       step_ratio=1,
                                       min_size=(60,60),
                                       max_size=(120, 120))

fig, ax = plt.subplots()
plt.imshow(image, cmap="gray")

for patch in detected:
    ax.add_patch(
        patches.Rectangle(
            (patch['c'], patch['r']),
            patch['width'],
            patch['height'],
            fill=False,
            color='r',
            linewidth=2
        )
    )

plt.show()