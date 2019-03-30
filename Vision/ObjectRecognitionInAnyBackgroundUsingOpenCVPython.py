import cv2
import numpy as np

# https://thecodacus.com/object-recognition-using-opencv-python/#.XJ55xJzgoeM
# http://jematoscv.blogspot.com/2014/05/matching-features-with-orb-using-opencv.html

detector = cv2.ORB() #FeatureDetector_create("ORB")#cv2.xfeatures2d.SIFT_create() #cv2.SIFT()
FLANN_INDEX_KDTREE = 0
flannParam = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
flann = cv2.FlannBasedMatcher(flannParam, {})
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

print("flann")

trainImg=cv2.imread("bob_logo.jpg")
gray = cv2.cvtColor(trainImg, cv2.COLOR_BGR2GRAY)
print("bob_logo")
#trainKP=detector.detect(gray,None)
print("detect")
#trainKP,trainDesc=detector.compute(gray,trainKP)
trainKP, trainDesc = detector.detectAndCompute(trainImg, None)
print("compute")

cam=cv2.VideoCapture(0)


while True:
    ret, QueryImgBGR = cam.read()
    queryImg = cv2.cvtColor(QueryImgBGR, cv2.COLOR_BGR2GRAY)
    print(queryImg)
    queryKP, queryDesc = detector.detectAndCompute(queryImg, None)

    if len(trainDesc) == 0:
        cvError(0, "MatchFinder", "Train descriptor empty", __FILE__, __LINE__);
    if len(queryDesc) == 0:
        cvError(0, "MatchFinder", "Query descriptor empty", __FILE__, __LINE__);

    #matches = flann.knnMatch(queryDesc, trainDesc, k=2)
    matches = bf.match(queryDesc,trainDesc)
    dist = [m.distance for m in matches]
    thres_dist = (sum(dist) / len(dist)) * 0.5
    goodMatch = [m for m in matches if m.distance < thres_dist]

    #goodMatch=[]
    #for m, n in matches:
    #    if(m.distance<0.75*n.distance):
    #        goodMatch.append(m)

    MIN_MATCH_COUNT=30
    print(len(goodMatch))
    if(len(goodMatch)>=MIN_MATCH_COUNT):
        tp=[]
        qp=[]

        for m in goodMatch:
            tp.append(trainKP[m.trainIdx].pt)
            qp.append(queryKP[m.queryIdx].pt)

        tp, qp = np.float32((tp, qp))

        H, status = cv2.findHomography(tp, qp, cv2.RANSAC, 3.0)

        h, w = trainImg.shape
        trainBorder = np.float32([[[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]])
        queryBorder = cv2.perspectiveTransform(trainBorder, H)
        cv2.polylines(QueryImgBGR, [np.int32(queryBorder)], True, (0, 255, 0), 5)
    else:
        print "Not Enough match found- %d/%d"%(len(goodMatch), MIN_MATCH_COUNT)
    cv2.imshow('result', QueryImgBGR)
    if cv2.waitKey(10) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
