import cv2
import numpy as np

class CircleDetection:

    background_colour = 255

    # Change colour to match illumination
    def normalise_rgb(self, target_colour):
        return self.background_colour * (target_colour / 255.0)

    def coordinate_convert(self, pixels):
        # Converts pixels into metres
        return np.array([(pixels[0] - self.env.viewerSize / 2) / self.env.resolution,
                         -(pixels[1] - self.env.viewerSize / 2) / self.env.resolution])

    def detect_blue(self, image):
        # Isolate the colour in the image as a binary image
        colour = self.normalise_rgb(255)
        lower_limit = colour - 100
        upper_limit = colour + 100
        mask = cv2.inRange(image, (lower_limit, 0, 0), (upper_limit, 100, 100))
        # detecting centre of circle

        kernel = np.ones((5, 5), np.uint8)
        # This applies a dilate that makes the binary region larger (the more iterations the larger it becomes)
        mask = cv2.dilate(mask, kernel, iterations=10)
        # erode to remove noise
        mask = cv2.erode(mask, kernel, iterations=10)

        cv2.imshow("circle", mask)
        cv2.waitKey(0)

        # Obtain the contours of the binary image
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        blob = contours[0]
        (x, y), radius = cv2.minEnclosingCircle(contours[0])

        return mask, np.array([x, y])


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    circle_detector = CircleDetection()

    for i in range(50):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # frame dimensions 480 X 640 X 3

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print("HSV {} BGR {}".format(frame_hsv[480/2][640/2],frame[480/2][640/2]))
        cv2.imshow("frame", frame)
        cv2.waitKey(0)

        #mask, coordinates = circle_detector.detect_blue(frame)

        #cv2.imshow("circle", mask)
        #cv2.waitKey(0)