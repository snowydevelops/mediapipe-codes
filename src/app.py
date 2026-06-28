import cv2
import mediapipe as mp

# مقداردهی MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# گرفتن تصویر از وبکم
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    # تبدیل رنگ
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # پردازش دست
    results = hands.process(frameRGB)

    # اگر دست تشخیص داده شد
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # رسم نقاط و اتصال‌ها
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # نمایش تصویر
    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()