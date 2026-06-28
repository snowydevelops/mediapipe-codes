import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
draw_util = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
finger_count_opened = 0
finger_count_closed = 0

while True:

    sucsess , frame = cap.read()

    if not sucsess:
        break

    finger_count_opened = 0
    finger_count_closed = 0
    framRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hands.process(framRGB)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            # draw_util.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmark = hand.landmark
            finger_tip_open = [8, 12]
            finger_tip_close = [16, 20]

            for tip in finger_tip_open:
                if landmark[tip].y < landmark[tip-2].y:
                    finger_count_opened +=1

            for  tip in finger_tip_close:
                if landmark[tip].y > landmark[tip-2].y:
                    finger_count_closed +=1

            if landmark[4].x < landmark[3].x:
                finger_count_closed +=1

    if finger_count_opened == 2 and finger_count_closed ==3:
        filename = './images/test_victory.png'
        cv2.imwrite(filename, frame)
        cv2.putText(frame, 'OK', (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 3 , (255,255,0), 3)
    else:
        cv2.putText(frame, 'NOT OK', (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 3 , (255,255,0), 3)


    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()