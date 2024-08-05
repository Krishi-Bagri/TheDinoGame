import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def get_angle(a, b, c):
    """ Calculate angle between three points """
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point (pivot)
    c = np.array(c)  # End point
    
    # Vector AB and BC
    ab = a - b
    bc = c - b
    
    # Calculate the angle using the dot product and magnitude
    dot_product = np.dot(ab, bc)
    magnitude_ab = np.linalg.norm(ab)
    magnitude_bc = np.linalg.norm(bc)
    angle = np.arccos(dot_product / (magnitude_ab * magnitude_bc))
    
    # Convert angle from radians to degrees
    angle = np.degrees(angle)
    
    return angle

# Initialize state
previous_action = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the BGR image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and detect pose
    results = pose.process(image)
    
    # Draw the pose annotation on the image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Extract landmarks
        landmarks = results.pose_landmarks.landmark
        
        # Get coordinates for legs
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        
        # Get coordinates for hands
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        
        # Calculate angles for legs
        left_leg_angle = get_angle(left_hip, left_knee, left_ankle)
        right_leg_angle = get_angle(right_hip, right_knee, right_ankle)
        
        # Calculate hand angle
        hand_angle = get_angle(left_shoulder, left_wrist, right_wrist)
        
        # Determine action based on leg angles and hand angle
        if left_leg_angle < 90 and right_leg_angle < 90:
            action = 'bend'
            cv2.putText(image, 'BEND', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        elif left_leg_angle > 160 and right_leg_angle > 160 and abs(left_shoulder[1] - left_wrist[1]) < 0.1 and abs(right_shoulder[1] - right_wrist[1]) < 0.1:
            action = 'jump'
            cv2.putText(image, 'JUMP', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        elif abs(left_shoulder[1] - right_shoulder[1]) < 0.1 and abs(left_wrist[1] - right_wrist[1]) < 0.1:
            # Hands parallel to the ground (this is an approximate condition)
            action = 'run'
            cv2.putText(image, 'RUN', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        else:
            action = 'run'
        
        # Perform action if it has changed
        if action != previous_action:
            print(f"Action: {action}")  # Debug print for action detection
            if action == 'jump':
                pyautogui.press('space')
                print("Pressed: space")  # Debug print for key press
            elif action == 'bend':
                pyautogui.press('down')
                print("Pressed: down")  # Debug print for key press
            # 'run' requires no action as it's the default state

            previous_action = action
    
    # Display the resulting frame
    cv2.imshow('MediaPipe Pose', image)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
