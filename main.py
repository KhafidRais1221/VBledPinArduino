import cv2
from cvzone.HandTrackingModule import HandDetector
import pyfirmata


cap = cv2.VideoCapture(1)
#cap.set(3, 1280)
#cap.set(4, 720)

detector = HandDetector(detectionCon=0.7)

counter_R, counter_Y, counter_G = 0, 0, 0
R_on, Y_on, G_on = False, False, False

valRYG = [0, 0, 0]

pinR, pinY, pinG = 2,3,4
port = "COM3"
board = pyfirmata.Arduino(port)

if cap.isOpened()==False:
    print("kamera tidak bisa diakses!!!")
    exit()

while cap.isOpened():
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bboxInfo = detector.findPosition(img)
    #print(lmlist)

    if lmlist:
        x, y = 20, 20
        w, h = 100, 100
        X, Y = 36, 70

        fx, fy = lmlist[8][0], lmlist[8][1]
        posFinger = [fx, fy]
        #print(posFinger)

        cv2.circle(img, (fx,fy),15,(255,255,0),cv2.FILLED)
        #cv2.putText(img, str(posFinger), (fx+15,fy-15), cv2.FONT_ITALIC, 1, (0,0,0), 3)

        if x < fx < x+w-15 and y < fy < y+h-15:
            counter_R += 1
            cv2.rectangle(img, (x, y), (w, h), (255, 255, 0), cv2.FILLED)
            if counter_R == 1:
                R_on = not R_on
        else:
            counter_R = 0
            if R_on:
                R_val = 1
                cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, "ON", (X, Y), cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
            else:
                R_val = 0
                cv2.rectangle(img, (x, y), (w, h), (0, 0, 0), cv2.FILLED)
                cv2.putText(img, "OFF", (X, Y), cv2.FONT_ITALIC, 1, (0, 0, 255), 3)

        if x < fx < x+w-15 and y+100 < fy < y+h-15+100:
            counter_Y += 1
            cv2.rectangle(img, (x, y+100), (w, h+100), (255, 255, 0), cv2.FILLED)
            if counter_Y == 1:
                Y_on = not Y_on
        else:
            counter_Y = 0
            if Y_on:
                Y_val = 1
                cv2.rectangle(img, (x, y+100), (w, h+100), (0, 255, 255), cv2.FILLED)
                cv2.putText(img, "ON", (X, Y+100), cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
            else:
                Y_val = 0
                cv2.rectangle(img, (x, y+100), (w, h+100), (0, 0, 0), cv2.FILLED)
                cv2.putText(img, "OFF", (X, Y+100), cv2.FONT_ITALIC, 1, (0, 255, 255), 3)

        if x < fx < x+w-15 and y+200 < fy < y+h-15+200:
            counter_G += 1
            cv2.rectangle(img, (x, y+200), (w, h+200), (255, 255, 0), cv2.FILLED)
            if counter_G == 1:
                G_on = not G_on
        else:
            counter_G = 0
            if G_on:
                G_val = 1
                cv2.rectangle(img, (x, y+200), (w, h+200), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "ON", (X, Y+200), cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
            else:
                G_val = 0
                cv2.rectangle(img, (x, y+200), (w, h+200), (0, 0, 0), cv2.FILLED)
                cv2.putText(img, "OFF", (X, Y+200), cv2.FONT_ITALIC, 1, (0, 255, 255), 3)

        #valRYG[0] = R_val
        #valRYG[1] = Y_val
        #valRYG[2] = G_val
        #print(valRYG)

        board.digital[pinR].write(R_val)
        board.digital[pinY].write(Y_val)
        board.digital[pinG].write(G_val)


        cv2.putText(img, "Created By: Arducomp", (10, 440), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 2)
        cv2.putText(img, "Date : 25/11/2021", (10, 470), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 2)

    cv2.imshow("image", img)
    cv2.waitKey(1)