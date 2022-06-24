from turtle import color
import cv2
import cvzone
import pickle
import numpy as np

#Video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)

width, height = 107, 48

#bringing back the positions to video feed after selection in ParkingSpacePicker file
def checkParkingSpace(imgProcessed):

    spaceCounter = 0

    for pos in posList:
        x,y = pos


        #now we will crop the image and find wheter there's a car inside it or not?
        imgCrop = imgProcessed[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), imgCrop)
        #now counting the pixels in cropped frame to that wheter there's a car in here or not based on pixel count
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x,y+height-3), scale= 1.5, thickness=2, offset=0, colorR= (13,166,196))

        #counting no of cars, setting threshold 900 pixels
        if count < 900:
            color = (128,255,0)
            thickness = 5
            spaceCounter += 1 
        else:
            color = (0,0,255)
            thickness = 2
            
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cvzone.putTextRect(img, str(spaceCounter) + " / " + str(len(posList)) + " Spaces are Available", (100,50), scale= 2, thickness=2, offset=20, colorR= (255,105,180))

#for each one of these crop photos we need to tell need to tell whether this region has a car present in it or not
# so how can we do that we can do that by looking at its pixel
# count so we need to convert this image into a
# binary image based on its uh edges and
# corners and then from there we can say that if it doesn't have a lot of edges
# or corners then if it's a plain image then it means there is no car but if it has then it
# means there is a car so how can we do that first of all we have to do some
# thresholding so to do some thresholding what we will do is after we get our
# image we are going to convert it into grayscale 


 
while True: 

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    #after blur converting it into binary image
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    #removing noise
    imgMedian = cv2.medianBlur(imgThreshold,5)
    # these pixels these values they might be a little bit thin
    # so what we can do is we can make it a little bit thicker so that it's easier to differentiate between empty spaces
    # and when there is a car so to do that we can use dilation so we
    # will use the morphology function
    kernel = np.ones((3,3), np.uint8)
    imgDialate = cv2.dilate(imgMedian, kernel, iterations= 1)


    checkParkingSpace(imgDialate)

  
  
   

 
 
    cv2.imshow("Image",img)
    # cv2.imshow("ImageBlur",imgBlur)
    # cv2.imshow("ImageThreshold",imgThreshold)
    cv2.waitKey(10)
