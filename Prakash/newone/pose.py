import cv2
import mediapipe as mp

# Initialize MediaPipe Pose solution
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize MediaPipe Hands solution for finger landmarks
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize MediaPipe Drawing utils
mp_drawing = mp.solutions.drawing_utils

# Custom Drawing Specs (Green color for all landmarks and connections)
green_style = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)

# Open the default camera (usually the first camera, index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the video stream!")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Blank frame grabbed!")
        break

    # Flip the frame horizontally for mirror view
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Pose (body landmarks)
    pose_results = pose.process(rgb_frame)

    # Process the frame with MediaPipe Hands (hand and finger landmarks)
    hand_results = hands.process(rgb_frame)

    # Draw body pose landmarks if detected
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            pose_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=green_style,
            connection_drawing_spec=green_style,
        )

    # Draw hand landmarks for each detected hand
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=green_style,
                connection_drawing_spec=green_style,
            )

    # Show the resulting frame
    cv2.imshow("Pose and Finger Detection with Green Color", frame)

    # Exit the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
