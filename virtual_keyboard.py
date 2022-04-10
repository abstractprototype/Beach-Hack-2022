from ast import Delete
import cv2
import cvzone
import mediapipe
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
# keyboard_keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
#                   ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
#                   ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
#                   ["1","2","3","4","5","6","7","8","9"],
#                   ["0","?","!","'","+","-","*"]
#                   ]

keyboard_keys = [["o"]]

final_text = ""

keyboard = Controller()


# def draw(img, buttonList):
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
        
#         cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0],button.size[0]), 20 ,rt=0)
#         cv2.rectangle(img, button.pos, (int(x + w), int(y + h)), (50, 50, 50), cv2.FILLED) #text box color #cv2.filled is our webcam playback

#         cv2.putText(img, button.text, (x + 20, y + 65),
#                     cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
#     return img


def transparent_layout(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1],button.size[0],button.size[0]), 20 ,rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]), (50, 50, 50), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 20, y + 65),cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
        #cv2.putText(imgNew, button.text, text_offset_x=20, text_offset_y=20, vspace=10, hspace=10, font_scale=1.0, background_RGB=(228,255,222),text_RGB=(255,255,1),thickness=1, alpha=0.5)

    out = img.copy()
    alpaha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpaha, imgNew, 1-alpaha, 0)[mask]
    return out


class Button():
    def __init__(self, pos, text="", size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

class DeleteButton(Button):
    def __init__(self, pos, previous, size=[85,85] ):
        self.pos = pos
        self.size = size

        



buttonList = []
# mybutton = Button([100, 100], "Q")
for k in range(len(keyboard_keys)):
    for x, key in enumerate(keyboard_keys[k]):
        buttonList.append(Button([100 * x + 25, 100 * k + 50], key))
        #print(x, key)


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = transparent_layout(img, buttonList)  # change the draw funtion to transparent_layout for transparent keys

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0]<x+w and y < lmList[8][1] < y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h),
                              (0, 255, 255), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                l, _, _ = detector.findDistance(8,12, img, draw=False)
                print(l)

                if l < 25:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h),
                                  (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                    final_text += button.text
                    sleep(0.20)

    # cv2.rectangle(img, (25,350), (700, 450),
    #               (255, 255, 255), cv2.FILLED)
    # cv2.putText(img, final_text, (60, 425),
    #             cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

    # cv2.rectangle(img, (100,100), (200,200),
    #               (100, 255, 0), cv2.FILLED)
    # cv2.putText(img, 'Q', (120,180), cv2.FONT_HERSHEY_PLAIN, 5,
    #             (0, 0, 0), 5)

    # img = mybutton.draw(img)
    cv2.imshow("output", img)
    cv2.waitKey(1)