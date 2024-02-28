import cv2
import numpy as np
import time
from handtracker import HandTracker

def main():
    # Initialize HandTracker
    hand_tracker = HandTracker()

    # Initialize camera
    cap = cv2.VideoCapture(0)  # Change to 1 if you're using an external camera

    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Find hands in the frame
        hand_tracker.find_hands(frame)

        black_screen = np.zeros_like(frame)

        # Overlay hand landmarks on the black screen
        if hand_tracker.results.multi_hand_landmarks:
            for hand_landmarks in hand_tracker.results.multi_hand_landmarks:
                hand_tracker.mp_draw.draw_landmarks(black_screen, hand_landmarks, hand_tracker.mp_hands.HAND_CONNECTIONS)

         # Display the black screen with hand landmarks
        # Draw FPS on the frame
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        cv2.putText(black_screen, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display the black screen with hand landmarks
        cv2.imshow('Hand Landmarks', black_screen)
        # Check for exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    hand_tracker.close()

if __name__ == "__main__":
    main()