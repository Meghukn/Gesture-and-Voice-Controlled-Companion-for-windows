import cv2
import mediapipe as mp
import os
import time
from collections import Counter

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Define tasks for each gesture
def perform_task(gesture_name):
    if gesture_name == "thumbs_up":
        os.system("start chrome")  # Opens Google Chrome
        print("Opening Chrome...")
    elif gesture_name == "victory":
        os.system(r'"C:\\Path\\To\\WhatsApp.exe"')  # Opens installed WhatsApp
        print("Opening WhatsApp...")
    elif gesture_name == "thumbs_down":
        os.system("start notepad")  # Opens Notepad
        print("Opening Notepad...")
    elif gesture_name == "call_sign":
        os.system("start ms-settings:")  # Opens Settings
        print("Opening Settings...")
    elif gesture_name == "open_palm":
        os.system("start calc")  # Opens Calculator
        print("Opening Calculator...")
    elif gesture_name == "ok_sign":
        os.system("start msedge")  # Opens Microsoft Edge
        print("Opening Microsoft Edge...")

# Helper function to detect gestures
def detect_gesture(landmarks):
    """
    Detects gestures based on hand landmarks.
    Returns the gesture name if detected, otherwise None.
    """
    thumb_tip = landmarks.landmark[4]
    thumb_mcp = landmarks.landmark[2]
    index_tip = landmarks.landmark[8]
    index_mcp = landmarks.landmark[5]
    middle_tip = landmarks.landmark[12]
    middle_mcp = landmarks.landmark[9]
    ring_tip = landmarks.landmark[16]
    ring_mcp = landmarks.landmark[13]
    pinky_tip = landmarks.landmark[20]
    pinky_mcp = landmarks.landmark[17]

    # Gesture: Thumbs Up
    if thumb_tip.y < thumb_mcp.y and all(
        finger.y > finger_mcp.y
        for finger, finger_mcp in zip(
            [index_tip, middle_tip, ring_tip, pinky_tip],
            [index_mcp, middle_mcp, ring_mcp, pinky_mcp],
        )
    ):
        return "thumbs_up"

    # Gesture: Thumbs Down
    if thumb_tip.y > thumb_mcp.y and all(
        finger.y > finger_mcp.y
        for finger, finger_mcp in zip(
            [index_tip, middle_tip, ring_tip, pinky_tip],
            [index_mcp, middle_mcp, ring_mcp, pinky_mcp],
        )
    ):
        return "thumbs_down"

    # Gesture: Victory (Index and Middle Raised)
    if (
        index_tip.y < index_mcp.y
        and middle_tip.y < middle_mcp.y
        and ring_tip.y > ring_mcp.y
        and pinky_tip.y > pinky_mcp.y
    ):
        return "victory"

    # Gesture: Call Sign (Thumb and Pinky Extended)
    if (
        thumb_tip.y < thumb_mcp.y
        and pinky_tip.y < pinky_mcp.y
        and all(
            finger.y > finger_mcp.y
            for finger, finger_mcp in zip(
                [index_tip, middle_tip, ring_tip],
                [index_mcp, middle_mcp, ring_mcp],
            )
        )
    ):
        return "call_sign"

    # Gesture: Open Palm (All fingers straight)
    if all(
        finger.y < finger_mcp.y
        for finger, finger_mcp in zip(
            [index_tip, middle_tip, ring_tip, pinky_tip],
            [index_mcp, middle_mcp, ring_mcp, pinky_mcp],
        )
    ) and thumb_tip.x < index_tip.x:
        return "open_palm"

    # Gesture: OK Sign (Thumb and Index Tip Touching)
    if (
        abs(thumb_tip.x - index_tip.x) < 0.02
        and abs(thumb_tip.y - index_tip.y) < 0.02
        and middle_tip.y < middle_mcp.y
        and ring_tip.y < ring_mcp.y
        and pinky_tip.y < pinky_mcp.y
    ):
        return "ok_sign"

    return None



# Main function to start the hand gesture recognition loop
def start_hand_gesture_recognition():
    # Initialize MediaPipe hands
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:

        cap = cv2.VideoCapture(0)

        # Buffer to store detected gestures for confirmation
        gesture_buffer = []
        buffer_size = 15  # Number of frames to confirm a gesture

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Flip the frame for a mirrored view
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect hands
            results = hands.process(rgb_frame)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Detect gesture
                    gesture = detect_gesture(hand_landmarks)
                    if gesture:
                        gesture_buffer.append(gesture)

                        # Maintain buffer size
                        if len(gesture_buffer) > buffer_size:
                            gesture_buffer.pop(0)

                        # Confirm gesture if consistent over buffer
                        most_common_gesture = Counter(gesture_buffer).most_common(1)[0]
                        if most_common_gesture[1] > buffer_size * 0.8:  # 80% consistency
                            perform_task(most_common_gesture[0])
                            print("Waiting for 3 seconds before closing...")
                            time.sleep(3)  # Camera stays open for 3 seconds
                            cap.release()  # Close the camera after performing the task
                            cv2.destroyAllWindows()
                            print("Camera closed. Run the program again to use it.")
                            return  # Return after finishing the task
            else:
                # Clear buffer if no hands are detected
                gesture_buffer = []

            # Display the video feed
            cv2.putText(frame, "Show Gesture: Thumbs Up, Victory, Thumbs Down, Call Sign, Open Palm, OK Sign", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("Hand Gesture Recognition", frame)

            # Break if 'q' is pressed
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()