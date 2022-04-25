import cv2
import mediapipe as mp
import time 

class handDetector():
    def __init__(self, mode=False, maxHands=2, complexity=1, detectionCon=0.75, trackCon=0.75):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, maxHands, complexity, detectionCon, trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.fungertips = [4, 8, 12, 16, 20]