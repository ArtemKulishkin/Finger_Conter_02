import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)#подключаемся к вэб-камере
mp_Hands = mp.solutions.hands #распознаем руки
# характеристики для распознования
hands = mp_Hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2)
mpDraw = mp.solutions.drawing_utils #утилита для рисования
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)] #координаты интересующих точек у пальцев(кроме большого)
thumb_Coord = (4, 3) #координаты интересующих точек большого пальца

# Получить информацию о размере кадрас помощью метода get()
#frame_width = 640
#frame_height = 480
#frame_size = (frame_width,frame_height)
# Инициализировать объект записи видео
#output = cv2.VideoWriter('output_video_from_file.mp4', cv2.VideoWriter_fourcc(* 'XVID'), 30, frame_size)

while cap.isOpened(): #пока камера "работает"
    success, image = cap.read() #получаем кадр с вэб-камеры(true/false)
    if not success: #если не удалось получить кадр
        print ("Не удалось")
        continue #переход к ближайшему циклу (while)
    
    image = cv2.flip(image, 1) #зеркалка
    #img2 = image.copy()
    #img2[:,:] = [0,0,0]

    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #BGR -> RGB
    result = hands.process(RGB_image) #ищем руки
    if result.multi_hand_landmarks: #если найдены руки
        multiLandMarks = result.multi_hand_landmarks #извлекаем список найденных рук
        upCount = 0
        for idx, handLms in enumerate(multiLandMarks):
            lbl = result.multi_handedness[idx].classification[0].label
            print(lbl)
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS) #рисуем маску руки
            handlist = []
            for lm in handLms.landmark:
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handlist.append((cx, cy))
            for coordinate in finger_Coord:
                if handlist[coordinate[0]][1] < handlist[coordinate[1]][1]:
                    upCount += 1

        print(upCount)
        cv2.putText(image, str(upCount), (100, 150), cv2.FONT_ITALIC, 8, (0, 220, 100), 8)
            #mpDraw.draw_landmarks(img2, handLms, mp_Hands.HAND_CONNECTIONS)
    
    
    #output.write(img2)
    #cv2.imshow('img.jpg', img2)
    cv2.imshow('image', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
#output.release()
