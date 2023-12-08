import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]
finalText = ""
keyboard = Controller()

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 15, y + 65), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    return img

# def drawAll(img, buttonList):
#     imgNew = np.zeros_like(img, np.int8)
#     for button in buttonList:
#         x, y = button.pos
#         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
#         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]), (255, 0, 255), cv2.FILLED)
#         cv2.putText(img, button.text, (x + 15, y + 65), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
#     out = img.copy()
#     alpha = 0.5
#     mask = imgNew.astype(bool)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
#     return out
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        for hand in hands:
            lmList = hand['lmList']
            bboxInfo = hand['bbox']

            img = drawAll(img, buttonList)

            if lmList:
                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size

                    if x <= lmList[8][0] <= x + w and y <= lmList[8][1] <= y + h:
                        cv2.rectangle(img, (x-5, y-5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 15, y + 65), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

                        if len(lmList) > 12:
                            x1, y1 = lmList[8][:2]  # Extract x and y values of lmList[8]
                            x2, y2 = lmList[12][:2]  # Extract x and y values of lmList[12]
                            l = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


                            # when clicked
                            if l <= 30:
                                keyboard.press(button.text)
                                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                                cv2.putText(img, button.text, (x + 15, y + 65), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                                finalText += button.text
                                sleep(0.60)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:
        break
print(finalText)
cap.release()
cv2.destroyAllWindows()
