import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
linestest = []
frame_width = cap.get(3)
frame_height = cap.get(4)


with mp_hands.Hands(max_num_hands=1) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        def checkinKunckle(cod, foreknuck, prinky1):
            if (
                cod[0] > foreknuck[0]
                and cod[0] < prinky1[0]
                and cod[1] > forefinger[1]
                and cod[1] < prinky1[1]
            ):
                return (-1, -1)
            return cod

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                position = results.multi_hand_landmarks[0].landmark
                forefinger = (
                    int(position[8].x * frame_width),
                    int(position[8].y * frame_height),
                )
                thumb = (
                    int(position[4].x * frame_width),
                    int(position[4].y * frame_height),
                )
                middle = (
                    int(position[12].x * frame_width),
                    int(position[12].y * frame_height),
                )
                foreknuck = (
                    int(position[6].x * frame_width),
                    int(position[6].y * frame_height),
                )
                pinkyknuck = (
                    int(position[18].x * frame_width),
                    int(position[18].y * frame_height),
                )
                prinky1 = (
                    int(position[0].x * frame_width),
                    int(position[0].y * frame_height),
                )
                # mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
                if (abs(forefinger[1] - middle[1])) < 60 and (
                    forefinger[1] - foreknuck[1] < 0
                ):
                    linestest.append(forefinger)
                    cv2.circle(image, forefinger, 10, (0, 0, 255), -1)
                elif (
                    forefinger[1] - foreknuck[1] > 0
                ):  # thumb[0] < 100 and thumb[1]<500:
                    linestest = [
                        checkinKunckle(cod, foreknuck, prinky1) for cod in linestest
                    ]
                else:
                    cv2.circle(image, forefinger, 10, (0, 0, 255), -1)
                    if len(linestest) > 0 and linestest[-1] != (-1, -1):
                        linestest.append((-1, -1))

        for i, cordes in enumerate(linestest):
            if cordes[0] == -1 and cordes[1] == -1:
                continue
            if i > 0 and linestest[i - 1][0] != -1 and linestest[i - 1][1] != -1:
                TODO = 1
                cv2.line(image, linestest[i - 1], linestest[i], (0, 0, 255), 2)

        cv2.imshow("Hand Tracking", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()

