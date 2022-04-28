import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, complexity=0, detectionCon=0.75, trackCon=0.75):
        self.mpHands = mp.solutions.hands  # хотим распознавать руки (hands)
        self.hands = self.mpHands.Hands(mode, maxHands, complexity, detectionCon, trackCon)
        self.mpDraw = mp.solutions.drawing_utils  # утилита для рисования
        self.fingertips = [4, 8, 12, 16, 20] # кончики пальцев
    
    def findHands(self, img, draw=True):
        RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR -> RGB
        RGB_image.flags.writeable = False
        self.result = self.hands.process(RGB_image)  # ищем руки
        RGB_image.flags.writeable = True
        if draw:
            if self.result.multi_hand_landmarks:
                for handLms in self.result.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img
    def findPosition(self, img, handNumber=0, draw=True):
        self.handList[handNumber] = None # Список координат пальцев в пикселях       
        if self.multi_hand_landmarks:  # если найдены 
            myHand = self.multi_hand_landmarks[handNumber]  # извлекаем список найденных рук
            for id, lm in enumerate(myHand.landmark):
                #преобразование координат из mp в пиксели
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handList.append((cx, cy))

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while cap.isOpened():  # пока камера "работает"
        success, image = cap.read()  # полчаем кадр с web-камеры (True/False, image)
        if not success:  # если не удалось получить кадр
            print("Не удалось получить изображение с web-камеры")
            continue  # переход к ближайшему циклу (while)
    
        image = cv2.flip(image, 1)  # зеркальное отражение картинкиwhile True:
        image = detector.findHands(image)
        cv2.imshow("Image", image)
        if cv2.waitKey(1) &  0xFF == 27:  # esc
            break

main()
