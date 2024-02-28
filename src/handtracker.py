import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.static_image_mode,
            max_num_hands=self.max_num_hands,
            model_complexity = 0,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def get_landmarks(self):
        if self.results.multi_hand_landmarks:
            return self.results.multi_hand_landmarks

    def display_image(self, frame, window_name='Hand Tracking'):
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

    def close(self):
        cv2.destroyAllWindows()