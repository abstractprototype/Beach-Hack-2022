from pickle import TRUE
import cv2
import cvzone
import mediapipe
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import random

from sqlalchemy import false
from playsound import playsound

# from pynput.keyboard import Controller


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keyboard_keys = [['Q','E','G','R','L','U','L','I'],
                 ['L','H','S','L','V','W','B','M'],
                 ['A','L','L','H','L','L','L','L'],
                 ['D','C','O','L','T','L','N','L']]


# keyboard = Controller()

def transparent_layout(img, button):
    imgNew = np.zeros_like(img, np.uint8)
    x, y = button.pos
    cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[0]), 20, rt=0)
    print(button.pos[0], button.pos[1], button.size[0], button.size[0])
    center = ((button.pos[0]+button.size[0])-43, (button.pos[1]+button.size[0])-43)
    cv2.circle(imgNew,center, 45, button.color, cv2.FILLED) #outside color
    cv2.putText(imgNew, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4) #inside color BGR

    out = img.copy()
    alpaha = 0.2
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpaha, imgNew, 1 - alpaha, 0)[mask]
    return out


class Button():
    def __init__(self, pos, text="", size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
        self.dy = random.randint(-25,25)
        self.dx = random.randint(-25,25)
        self.color = random.randint(0,255),random.randint(0,255),random.randint(0,255)

buttonList = []

for k in range(len(keyboard_keys)):
    for x, key in enumerate(keyboard_keys[k]):
        buttonList.append(Button([100 * x + 25, 100 * k + 50], key))

inProgress = False
isOver = False
num = 0
duration = 0
durCount = 0

score = 0
counter = 0
endtimer = 0
endcount = 0

while isOver == False:
    success, img = cap.read()
    height = img.shape[0]
    width = img.shape[1]
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    if inProgress == True:
        if(duration == 0 and inProgress == True):
            duration = 300
        cv2.putText(img, 'Timer: ' + str(duration - durCount), (350, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)
        durCount = durCount + 1
        if durCount > duration:
            isOver = True
        
        # button = buttonList[num]
        for button in buttonList[:5]:

            # button.pos[1] += button.dy
            img = transparent_layout(img, button)
            print("button:",button.text)
            center = ((button.pos[0] + button.size[0]) - 43, (button.pos[1] + button.size[0]) - 43)
        
            if (isOver == False):
                cv2.putText(img, 'Your Bitcoin: ' + str(score), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            elif (isOver == True):
                cv2.putText(img, 'Your Bitcoin: ' + str(score), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(img, ' GAME OVER ', (320, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5, cv2.LINE_AA)

            x, y = button.pos
            w, h = button.size
            if y <= 0 or y+h >= height:
                button.dy *= -1
            if x <= 0 or x+w >= width:
                button.dx *= -1
            button.pos[0] += button.dx
            button.pos[1] += button.dy

            if lmList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.circle(img, center, 45, (0, 225, 225), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    print(l)

                    if l < 25:
                        # keyboard.press(button.text)
                        score += 1

                        playsound('coin.wav')

                        buttonList.remove(button)
                        cv2.circle(img, center, 45, (0, 255, 225), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                        # final_text += button.text
                        #sleep(0.5)
                        num = random.randint(0, len(buttonList)-1)
                        #buttonList.append(Button([100 * num + 25, 100 * abs(num-20) + 50], key))



    elif (inProgress == False):
        time = 30
        cv2.putText(img, 'GAME WILL START IN --> ' + str(time - counter) + " Grab as many Bitcoin as you can!!!", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 3, cv2.LINE_AA)
        counter = counter + 1
        if counter > time:
            inProgress = True


    cv2.imshow("output", img)
    cv2.waitKey(1) #framerate

sleep(5)