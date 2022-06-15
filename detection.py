import skimage
import matplotlib.pyplot as plt
from skimage import io
from skimage.feature import Cascade
from matplotlib import patches

def detectFaces(image, size):
    # Charge le fichier contenant le modèle préentraîné
    trained = skimage.data.lbp_frontal_face_cascade_filename()

    # Détecteur
    detector = Cascade(trained)
    detected = detector.detect_multi_scale(image, scale_factor=1.2,
                                        step_ratio=1,
                                        min_size=(size[0], size[0]),
                                        max_size=(size[1], size[1]))

    _, ax = plt.subplots()

    if __name__ == '__main__':
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
        
    facesCoords = []
    for patch in detected:
        facesCoords.append((patch['c'], patch['r'], patch['width'], patch['height']))
    return facesCoords

if __name__ == '__main__':
    testImage = io.imread("test-image.jpg")
    print(detectFaces(testImage, 300))