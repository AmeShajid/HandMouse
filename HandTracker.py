#this is to test the hand tracking and mouse control


import cv2  # Importing the OpenCV library for computer vision tasks.
import mediapipe as mp  # Importing the Mediapipe library for hand tracking.
import pyautogui  # Importing the PyAutoGUI library for controlling the mouse and keyboard.
cap = cv2.VideoCapture(0)  # Initializing the webcam capture object.
hand_detector = mp.solutions.hands.Hands()  # Creating a hand detection object.
drawing_utils = mp.solutions.drawing_utils  # Creating a drawing utility object for visualization.
screen_width, screen_height = pyautogui.size()  # Getting the screen resolution.
index_y = 0  # Initializing the y-coordinate of the index finger.

# Loop for continuously capturing frames from the webcam.
while True:
    _, frame = cap.read()  # Reading a frame from the webcam.
    frame = cv2.flip(frame, 1)  # Flipping the frame horizontally.
    frame_height, frame_width, _ = frame.shape  # Getting the dimensions of the frame.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converting the frame to RGB format.
    output = hand_detector.process(rgb_frame)  # Processing the frame for hand detection.
    hands = output.multi_hand_landmarks  # Extracting hand landmarks from the output.
    
    if hands:  # If hands are detected in the frame.
        for hand in hands:  # Iterating through each detected hand.
            drawing_utils.draw_landmarks(frame, hand)  # Drawing landmarks on the frame.
            landmarks = hand.landmark  # Extracting landmarks of the hand.
            
            for id, landmark in enumerate(landmarks):  # Iterating through each landmark.
                x = int(landmark.x * frame_width)  # Calculating x-coordinate of the landmark.
                y = int(landmark.y * frame_height)  # Calculating y-coordinate of the landmark.
                
                if id == 8:  # If the landmark corresponds to the tip of the index finger.
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))  # Drawing a circle at the index finger tip.
                    index_x = screen_width / frame_width * x  # Mapping x-coordinate to screen resolution.
                    index_y = screen_height / frame_height * y  # Mapping y-coordinate to screen resolution.

                if id == 4:  # If the landmark corresponds to the tip of the thumb.
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))  # Drawing a circle at the thumb tip.
                    thumb_x = screen_width / frame_width * x  # Mapping x-coordinate to screen resolution.
                    thumb_y = screen_height / frame_height * y  # Mapping y-coordinate to screen resolution.
                    print('outside', abs(index_y - thumb_y))  # Printing the distance between index and thumb tips.
                    
                    if abs(index_y - thumb_y) < 20:  # If distance is small, indicating a click gesture.
                        pyautogui.click()  # Simulating a mouse click.
                        pyautogui.sleep(1)  # Adding a small delay.
                    elif abs(index_y - thumb_y) < 100:  # If distance is moderate, moving the mouse.
                        pyautogui.moveTo(index_x, index_y)  # Moving the mouse pointer.
    
    cv2.imshow('Virtual Mouse', frame)  # Displaying the frame with hand landmarks.
    cv2.waitKey(1)  # Waiting for a key press.
