import cv2
import cvzone
import mediapipe
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import random
import random

# from pynput.keyboard import Controller


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=1)

score = 0
counter = 0

keyboard_keys = [["o","o","o","o","o","o"],["o","o","o","o","o","o"],["o","o","o","o","o","o"],["o","o","o","o","o","o"]]


# keyboard = Controller()

def transparent_layout(img, button):
    imgNew = np.zeros_like(img, np.uint8)
    x, y = button.pos
    cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[0]), 20, rt=0)
    cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]), (50, 50, 50), cv2.FILLED)
    cv2.putText(imgNew, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

    out = img.copy()
    alpaha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpaha, imgNew, 1 - alpaha, 0)[mask]
    return out


class Button():
    def __init__(self, pos, text="", size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []

for k in range(len(keyboard_keys)):
    for x, key in enumerate(keyboard_keys[k]):
        buttonList.append(Button([100 * x + 25, 100 * k + 50], key))

inProgress = False
isOver = False
num = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    if inProgress == True:
        button = buttonList[num]
        img = transparent_layout(img, button)
        print(num)
        print("button pos:",button.pos)
        if (isOver == False):
            cv2.putText(img, 'SCORE: ' + str(score), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        elif (isOver == True):
            cv2.putText(img, ' GAME OVER ', (320, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5, cv2.LINE_AA)

        if lmList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h),
                              (0, 255, 255), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                if l < 25:
                    # keyboard.press(button.text)
                    score += 1
                    cv2.rectangle(img, button.pos, (x + w, y + h),
                                  (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                    # final_text += button.text
                    #sleep(0.5)
                num = random.randint(0,len(buttonList)-1)
                buttonList.append(Button([100 * num + 25, 100 * int(num%2) + 50], key))



    elif (inProgress == False):
        time = 50
        cv2.putText(img, 'GAME WILL START IN --> ' + str(time - counter), (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 3, cv2.LINE_AA)
        counter = counter + 1
        if counter > time:
            inProgress = True

    cv2.imshow("output", img)
    cv2.waitKey(1)
