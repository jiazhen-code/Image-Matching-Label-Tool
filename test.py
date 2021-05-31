import cv2
import numpy as np
import os
import warnings
import matplotlib.pyplot as plt

test_im = r'C:\Users\ljz\Desktop\match\image\1001_Z2203_a0.jpg'
txt_file = r'C:\Users\ljz\Desktop\match\save\1001_Z2203_a0.txt'

if os.path.exists(test_im) and os.path.exists(txt_file):
    im = cv2.imread(test_im, 1)
    with warnings.catch_warnings():

        warnings.simplefilter('ignore')
        raw = np.loadtxt(txt_file)
        if len(raw.shape) == 1:
            raw = raw[np.newaxis, :]
        try:
            raw[:, 0] *= float(im.shape[1])
            raw[:, 1] *= float(im.shape[0])
            for x, y in raw:
                cv2.circle(im, (int(x), int(y)), 5, (255, 255, 255), 3)
        except Exception as e:
            print(str(e))


    plt.figure(dpi=300)
    plt.imshow(im)
    plt.show()