import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
draw_util = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
finger_count = 0

while True:

    sucsess , frame = cap.read()

    if not sucsess:
        break

    finger_count = 0
    framRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hands.process(framRGB)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            # draw_util.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmark = hand.landmark
            finger_tip = [8, 12, 16 , 20]
            for tip in finger_tip:
                if landmark[tip].y > landmark[tip-2].y:
                    finger_count +=1

            if landmark[4].x < landmark[3].x:
                finger_count +=1

    if finger_count == 5:
        cv2.putText(frame, 'OK', (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 3 , (255,255,0), 3)
    else:
        cv2.putText(frame, 'NOT OK', (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,0), 3)


    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()