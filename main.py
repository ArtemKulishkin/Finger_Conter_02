import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1)
mpDraw = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4, 2)


 # Получить информацию о размере кадра с помощью метода get()
frame_width = 640
frame_height = 480
frame_size = (frame_width,frame_height)
# Инициализировать объект записи видео
output = cv2.VideoWriter('output_video_from_file.mp4', cv2.VideoWriter_fourcc(* 'XVID'), 30, frame_size)

while cap.isOpened(): 
    success, image = cap.read()
    if not success:
        print ("Не удалось")
        continue
    
    image = cv2.flip(image, 1)
    img2 = image.copy()
    img2[:,:] = [0,0,0]

    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(RGB_image)
    if result.multi_hand_landmarks:
        multiLandMarks = result.multi_hand_landmarks
        for idx, handLms in enumerate(multiLandMarks):
            lbl = result.multi_handedness[idx].classification[0].label
            print(lbl)
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            mpDraw.draw_landmarks(img2, handLms, mp_Hands.HAND_CONNECTIONS)
    
    
    output.write(img2)
    #cv2.imshow('img.jpg', img2)
    cv2.imshow('image', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
#output.release()
