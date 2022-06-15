from skimage import filters
import numpy as np

def Blurring(image,column, row, width, height):
    yMin, yMax = column, column + width
    xMin, xMax = row, row + height
    face = image[xMin:xMax, yMin:yMax]
    filtered = filters.gaussian(face, sigma=10)
    filtered = np.round(255 * filtered)
    image[xMin:xMax, yMin:yMax] = filtered
    return image

if __name__ == '__main__':
    import skimage
    import matplotlib.pyplot as plt
    from FaceBlurring import *
    from skimage import io
    from skimage.feature import Cascade
    from skimage import data, exposure
    from matplotlib import patches
    from skimage import filters
    # Charge le fichier contenant le modèle préentraîné
    trained = skimage.data.lbp_frontal_face_cascade_filename()

    # Détecteur
    detector = Cascade(trained)

    image = data.astronaut()

    detected = detector.detect_multi_scale(image,scale_factor=1.2,
                                           step_ratio=1,
                                           min_size=(60,60),
                                           max_size=(120, 120))

    fig, ax = plt.subplots()
    #plt.imshow(image, cmap="gray")

    filtered_img = image
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
        filtered_img = Blurring(filtered_img, patch['c'], patch['r'],patch['width'],patch['height'])





    plt.imshow(filtered_img, cmap="gray")
    plt.show()