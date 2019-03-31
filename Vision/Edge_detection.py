import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)
cap_width = cap.get(3)
cap_height = cap.get(4)

for i in range(5000):
    # Capture frame-by-frame
    ret, frame = cap.read()
    edges = cv2.Canny(frame,100,200)
    #print(edges)

    #plt.subplot(121),plt.imshow(frame,cmap = 'gray')
    #plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    #plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    #plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    #plt.show()

    kernel = np.ones((5, 5), np.uint8)
    # This applies a dilate that makes the binary region larger (the more iterations the larger it becomes)
    mask = cv2.dilate(edges, kernel, iterations=5)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    cv2.imshow('edges', edges)
    cv2.waitKey(1)
    cv2.imshow('mask', mask)
    cv2.waitKey(1)

    # Find contours
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    try:
        # Centre of largest contour
        obj = contours[0]
        centre = np.reshape(np.mean(obj, 0, dtype=np.int), 2)
    except IndexError:
        print('no object visible')
        centre = [-1,-1]

    if centre[0] > cap_width/3 and centre[0] < cap_width*2/3:
        print('YEET')
    else:
        print('NEET')



