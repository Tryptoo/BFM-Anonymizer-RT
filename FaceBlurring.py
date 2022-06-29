from skimage import filters
import numpy as np
import cv2
def Blurring(image, faceTab, blurFactor):
    yMin, yMax = faceTab[0], faceTab[2]
    xMin, xMax = faceTab[1], faceTab[3]
    face = image[xMin:xMax, yMin:yMax]
    filtered = filters.gaussian(face, sigma=blurFactor)
    filtered = np.round(255 * filtered)
    if __name__ == '__main__':
        image[xMin:xMax, yMin:yMax] = filtered
        return image
    return filtered

def BlurringCV(image, faceTab, blurFactor):
    yMin, yMax = faceTab[0], faceTab[2]
    xMin, xMax = faceTab[1], faceTab[3]
    face = image[xMin:xMax, yMin:yMax]
    height, width = face.shape[:2]
    temp = cv2.resize(face,(16,16), interpolation=cv2.INTER_LINEAR)
    filtered = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    if __name__ == '__main__':
        image[xMin:xMax, yMin:yMax] = filtered
        return image
    return filtered

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
        #filtered_img = Blurring(filtered_img, patch['c'], patch['r'],patch['width'],patch['height'])


    plt.imshow(filtered_img, cmap="gray")
    plt.show()