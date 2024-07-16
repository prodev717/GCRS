import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComplexity = modelComplexity
        self.mpStyle = mp.solutions.drawing_styles
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, bg, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS, self.mpStyle.get_default_pose_landmarks_style())
                    self.mpDraw.draw_landmarks(bg, handLms,self.mpHands.HAND_CONNECTIONS, self.mpStyle.get_default_pose_landmarks_style())
        return img

    def findPosition(self, img, handNo=0, draw=False):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 8, (0, 0, 255), cv2.FILLED)

        return lmList



def main():
    pTime = 0
    cTime = 0
    vid = cv2.VideoCapture(0)
    detector = handDetector()
    bg = 0
    while True:
        success, img = vid.read()
        img = detector.findHands(img,bg)
        lmList = detector.findPosition(img)
        if len(lmList) !=0:
            print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3,(255, 0, 255), 3)
        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def map_range(old_val, old_min, old_max, new_min, new_max):
    new_val = float(((old_val - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min)
    return new_val


if __name__ == "__main__":
    main()
