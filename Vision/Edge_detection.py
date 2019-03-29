import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)
for i in range(50):
    # Capture frame-by-frame
    ret, frame = cap.read()
    edges = cv2.Canny(frame,100,200)
    print(edges)

    plt.subplot(121),plt.imshow(frame,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()
