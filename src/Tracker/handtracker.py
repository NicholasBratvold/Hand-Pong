import cv2
import mediapipe as mp


class HandTracker:
    """
    A class that performs hand tracking using the MediaPipe library.

    Args:
        static_image_mode (bool): Whether to treat the input as a static image or a video stream. Default is False.
        max_num_hands (int): Maximum number of hands to detect. Default is 2.
        min_detection_confidence (float): Minimum confidence value for hand detection to be considered successful. Default is 0.5.
        min_tracking_confidence (float): Minimum confidence value for hand tracking to be considered successful. Default is 0.5.
    """

    def __init__(
        self,
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # If game is slow, change model_complexity to 0
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.static_image_mode,
            max_num_hands=self.max_num_hands,
            model_complexity=1,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        """
        Finds and tracks hands in the given frame.

        Args:
            frame (numpy.ndarray): The input frame in BGR format.
            draw (bool): Whether to draw the hand landmarks on the frame. Default is True.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

    def get_landmarks(self):
        """
        Returns the landmarks of the detected hands.

        Returns:
            list: A list of hand landmarks if hands are detected, otherwise None.
        """
        if self.results.multi_hand_landmarks:
            return self.results.multi_hand_landmarks

    def display_image(self, frame, window_name="Hand Tracking"):
        """
        Displays the image frame in a window.

        Args:
            frame (numpy.ndarray): The input frame in BGR format.
            window_name (str): The name of the window. Default is 'Hand Tracking'.
        """
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

    def close(self):
        """
        Closes all the open windows.
        """
        cv2.destroyAllWindows()


class FaceTracker:
    """
    A class that performs face detection using the MediaPipe library.

    Args:
        min_detection_confidence (float): Minimum confidence value for face detection to be considered successful. Default is 0.5.
    """

    def __init__(self, min_detection_confidence=0.5):
        self.min_detection_confidence = min_detection_confidence
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=self.min_detection_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_faces(self, frame, draw=True):
        """
        Finds and tracks faces in the given frame.

        Args:
            frame (numpy.ndarray): The input frame in BGR format.
            draw (bool): Whether to draw the face detections on the frame. Default is True.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.face_detection.process(frame_rgb)
        if self.results.detections and draw:
            for detection in self.results.detections:
                self.mp_draw.draw_detection(frame, detection)

    def get_landmarks(self):
        """
        Returns the landmarks of the detected faces.

        Returns:
            list: A list of face landmarks if faces are detected, otherwise None.
        """
        if self.results.detections:
            return self.results.detections

    def display_image(self, frame, window_name="Face Detection"):
        """
        Displays the image frame in a window.

        Args:
            frame (numpy.ndarray): The input frame in BGR format.
            window_name (str): The name of the window. Default is 'Face Detection'.
        """
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

    def close(self):
        """
        Closes all the open windows.
        """
        cv2.destroyAllWindows()
