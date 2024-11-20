import pickle
import cv2
import mediapipe as mp
import numpy as np
from pygame import mixer  # Add this import
import time  # Add this import

# Initialize pygame mixer
mixer.init()
# Load your drum and bass song (replace with your song path)
dnb_song = mixer.Sound('./dnbsong.mp3')  # Replace with your song path
is_playing = False  # Track if song is currently playing

# Add these variables after other initializations
dnb_start_time = None  # Track when DNB gesture starts
DNB_THRESHOLD = 1.0  # Second(s) to hold gesture before playing

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Try different camera indices
def get_working_camera():
    for index in range(2):  # Try indices 0 and 1
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"Successfully opened camera at index {index}")
                return cap
            cap.release()
    return None

cap = get_working_camera()

if cap is None:
    print("Error: Could not find a working camera. Please check your camera connection.")
    exit()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {36: 'DRUM N BASS', 1: 'B', 2: 'C', 3: 'D', 4: 'E', -1: 'None'}

current_sentence = []
current_letter = None
display_sentence = ""

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()
    
    # Add check if frame was successfully read
    if not ret or frame is None:
        print("Error: Could not read frame.")
        break

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        # Only process the first hand detected
        hand_landmarks = results.multi_hand_landmarks[0]
        
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

        for i in range(len(hand_landmarks.landmark)):
            x = hand_landmarks.landmark[i].x
            y = hand_landmarks.landmark[i].y
            x_.append(x)
            y_.append(y)

        for i in range(len(hand_landmarks.landmark)):
            x = hand_landmarks.landmark[i].x
            y = hand_landmarks.landmark[i].y
            data_aux.append(x - min(x_))
            data_aux.append(y - min(y_))

        try:
            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction = model.predict([np.asarray(data_aux)])
            predicted_label = int(prediction[0])
            
            # Check if prediction is in our known labels (0-4)
            if predicted_label not in range(0,36):
                predicted_label = -1
                
            predicted_character = labels_dict[predicted_label]
            current_letter = predicted_character  # Store the current prediction

            # Handle drum and bass playback with delay
            if predicted_character == 'DRUM N BASS':
                if dnb_start_time is None:
                    dnb_start_time = time.time()
                elif time.time() - dnb_start_time >= DNB_THRESHOLD and not is_playing:
                    dnb_song.play(-1)
                    is_playing = True
            else:
                dnb_start_time = None
                if is_playing:
                    dnb_song.stop()
                    is_playing = False

            # Add visual feedback for gesture timing
            if dnb_start_time is not None:
                hold_time = time.time() - dnb_start_time
                if hold_time < DNB_THRESHOLD:
                    progress = int((hold_time / DNB_THRESHOLD) * 100)
                    cv2.putText(frame, f"Hold: {progress}%", (x1, y2 + 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)
        except ValueError as e:
            print(f"Prediction error: {e}")
            continue

    # Display the current sentence at the top of the frame
    cv2.putText(frame, f"Sentence: {' '.join(current_sentence)}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    
    cv2.imshow('frame', frame)
    
    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' ') and current_letter and current_letter != 'None':
        # Add current letter to sentence when space is pressed
        current_sentence.append(current_letter)
    elif key == ord('b'):
        # Remove last letter when 'b' is pressed (backspace)
        if current_sentence:
            current_sentence.pop()

# Make sure to stop the song when quitting
if is_playing:
    dnb_song.stop()
cap.release()
cv2.destroyAllWindows()