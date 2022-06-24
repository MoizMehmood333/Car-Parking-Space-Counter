import cv2
import pickle

 #defining the shape of rectangle
width, height = 107, 48
 
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []
 


#for creating box on click or remove it 
def mouseClick(events, x, y, flags, params):
    #to add a box
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        #to remove a box
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            #if the right button is clicked inside the box

            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    #saving parking positions using pickle library in a file name "carParkPositions"
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)
 
 
while True:
    img = cv2.imread('carParkImg.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
 
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)








