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

    kernel = np.ones((5, 5), np.uint8)
    # This applies a dilate that makes the binary region larger (the more iterations the larger it becomes)
    mask = cv2.dilate(mask, kernel, iterations=5)

    # Find contours
    _, contours, _ = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Centre of largest contour
    obj = contours[0]
    centre = np.reshape(np.mean(obj, 0, dtype=np.int), 2)

