#! /usr/bin/env python3
import cv2
import numpy as np
from followLine import FollowLine

cap = cv2.VideoCapture(0)
cap_width = cap.get(3)
cap_height = cap.get(4)
OBJECT_THRESHOLD = 0.2 #

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
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        # find the biggest area
        obj = max(contours, key=cv2.contourArea)
        centre = np.reshape(np.mean(obj, 0, dtype=np.int), 2)
    else:
        print('no object visible')
        centre = [-1,-1]

    print(centre)
    line_follower = FollowLine()

    #if contours.[0[]

    if centre[0] < cap_width*1/4:
        # TODO: move forward
    elif centre[0] > cap_width*3/4:
        # TODO: move backward





