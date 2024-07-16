import cv2
import htm
from htm import map_range
import numpy as np
import math
import pyfirmata
import time

def servo_initNend():
    board.servo_config(9, 544, 2400, 90)
    board.servo_config(10, 544, 2400, 90)

def config_servo():
    if 25 < dis < 130:
        base = map_range(posLis[5][1], 640, 0, 0, 180)
        s1 = map_range(posLis[5][2], 480, 0, 0, 180)
        Ndis = map_range(dis, 130, 25, 30, 130)
        cv2.putText(bg, "depth : " + str(int(Ndis)) + " cm", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        board.servo_config(9, 544, 2400, base)
        board.servo_config(10, 544, 2400, s1)

cam = cv2.VideoCapture(0)
hands = htm.handDetector()
board = pyfirmata.Arduino("COM3")
bg = np.zeros((480, 640, 3), np.uint8)
servo_initNend()
time.sleep(3)

while cam.isOpened():
    frame, vid = cam.read()
    vid = cv2.cvtColor(cv2.flip(vid, 1), cv2.COLOR_BGR2RGB)
    vid = cv2.cvtColor(vid, cv2.COLOR_RGB2BGR)
    hands.findHands(vid, bg)
    posLis = hands.findPosition(vid, handNo=0, draw=False)
    if len(posLis) != 0:
        dis = math.sqrt(((posLis[5][2] - posLis[17][2]) ** 2) + ((posLis[5][1] - posLis[17][1]) ** 2))
        config_servo()
        if math.hypot(posLis[8][1]-posLis[4][1],posLis[8][2]-posLis[4][2])<20:
        	board.digital[7].write(1)
        else:
        	board.digital[7].write(0)
    cv2.imshow("bg", bg)
    cv2.imshow("cam", vid)
    bg = np.zeros((480, 640, 3), np.uint8)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        servo_initNend()
        break
