import numpy as np
import cv2

cap = cv2.VideoCapture(0)

cap_width = int(cap.get(3))
cap_height = cap.get(4)

DETECTION_THRESHOLD = 0.5 # percentage of window that has to be blue
WINDOW_SIZE = int(cap_height/4)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # we yeet the colour range to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Range for blue
    lower_blue = np.array([200/2., 120, 70])
    upper_blue = np.array([270/2., 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((5, 5), np.uint8)
    # This applies a dilate that makes the binary region larger (the more iterations the larger it becomes)
    mask = cv2.dilate(mask, kernel, iterations=5)
    # erode to remove noise
    mask = cv2.erode(mask, kernel, iterations=5)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.waitKey(1)
    cv2.imshow('game', mask)
    cv2.waitKey(1)

    # chamfer matching
    window = mask[-WINDOW_SIZE:] / 255
    template = np.ones((WINDOW_SIZE, cap_width))
    print(np.size(template[:,0]))
    cv2.imshow('window', window)
    cv2.waitKey(1)

    above_treshold = np.sum(window) > DETECTION_THRESHOLD * np.sum(template)
    print(above_treshold)





