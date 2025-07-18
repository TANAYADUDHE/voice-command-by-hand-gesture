import cv2
import mediapipe as mp
import pygame


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

pygame.mixer.init()

cap=cv2.VideoCapture(0)

finger_tips = [8,12,16,20]
thumb_tip = 4
last_alert = None

def count_fingers(hand_landmarks):
    fingers = []

    if hand_landmarks.landmark[thumb_tip].y < hand_landmarks.landmark[thumb_tip - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
    else:
        fingers.append(0)
    return sum(fingers)

def play_sound(file):
    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing sound:{e}")

while True:
    ret,frame, = cap.read()
    if not ret:
        break
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results =hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)
            finger_up = count_fingers(hand_landmarks)
            cv2.putText(frame,f'Fingers: {finger_up}',(10,50), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0),2)
            print(f'finger up: {finger_up}',end='\r')

            if finger_up == 1 and last_alert !=1:
                play_sound('audio 1.mp3')
                last_alert = 1

            elif finger_up == 2 and last_alert != 2:
                play_sound('audio2.mp3')
                last_alert = 2

            elif finger_up == 3 and last_alert != 3:
                play_sound('audio3.mp3')
                last_alert =3
            

            elif finger_up not in [1,2,3]:
                last_alert = None

    cv2.imshow('Hand Gesture', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()