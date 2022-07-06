
import mediapipe as mp
import cv2
class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self,image):
        lmlist = []
        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) > 1:
                LeftHand = self.results.multi_hand_landmarks[0]
                RightHand = self.results.multi_hand_landmarks[1]
                for id, lm in enumerate(RightHand.landmark):
                    h,w,c = image.shape
                    cx,cy = int(lm.x*w), int(lm.y*h)
                    lmlist.append([id,cx,cy])
                    #for list in lmlist:
                    #   cv2.putText(image,str(list[0]),(list[1],list[2]),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,0,255),2)
                for id, lm in enumerate(LeftHand.landmark):
                    h,w,c = image.shape
                    cx,cy = int(lm.x*w), int(lm.y*h)
                    lmlist.append([id,cx,cy])
                    #for list in lmlist:
                    #   cv2.putText(image,str(list[0]),(list[1],list[2]),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,0,255),2)
            else:
                Hand = self.results.multi_hand_landmarks[0]
                for id, lm in enumerate(Hand.landmark):
                    h,w,c = image.shape
                    cx,cy = int(lm.x*w), int(lm.y*h)
                    lmlist.append([id,cx,cy])
                    #for list in lmlist:
                    #   cv2.putText(image,str(list[0]),(list[1],list[2]),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,0,255),2)

        return lmlist

    def fingersUp(self):
        fingers = []

        #Thumb
        if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #4 Fingers
        for id in range(1, 5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers