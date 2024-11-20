import pickle
import cv2
import mediapipe as mp
import numpy as np
from pygame import mixer  # Add this import
import time  # Add this import
import google_tr

# Initialize pygame mixer
mixer.init()
# Load your drum and bass song (replace with your song path)
dnb_song = mixer.Sound('./dnbsong.mp3')  # Replace with your song path
is_playing = False  # Track if song is currently playing

# Add these variables after other initializations
dnb_start_time = None  # Track when DNB gesture starts
letter_start_time = None  # Track when a letter gesture starts
current_prediction = None  # Track the current prediction
LETTER_HOLD_THRESHOLD = 1.0  # Second(s) to hold letter before adding to sentence
DNB_THRESHOLD = 1.0  # Second(s) to hold gesture before playing
is_recording = False
current_sentence = []
sentences = []  # Array to store complete sentences

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

labels_dict = {
    0: 'H',
    1: 'E',
    2: 'L',
    3: 'O',
    4: 'DRUM N BASS',
    5: 'Stop',
    -1: 'None'
}

sentence_array = []  # Store the sentence as an array of letters
max_display_chars = 30  # Maximum characters to show at once

current_letter = None

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
            
            # Modified label handling
            try:
                predicted_character = labels_dict[predicted_label]
            except KeyError:
                # Handle unknown labels by treating them as 'None'
                predicted_label = -1
                predicted_character = 'None'
                
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
                if is_playing and predicted_character == 'Stop':
                    dnb_song.stop()
                    is_playing = False

            # Handle letter detection and holding
            if predicted_character not in ['DRUM N BASS', 'Stop', 'None']:
                if current_prediction != predicted_character:
                    letter_start_time = time.time()
                    current_prediction = predicted_character
                elif letter_start_time is not None:
                    hold_time = time.time() - letter_start_time
                    if hold_time >= LETTER_HOLD_THRESHOLD:
                        if is_recording:  # Only add to current_sentence if recording
                            current_sentence.append(predicted_character)
                            print(f"Added letter: {predicted_character}")  # Debug print
                        letter_start_time = None
                        current_prediction = None  # Reset prediction after adding letter
            else:
                letter_start_time = None
                current_prediction = None

            # Add visual feedback for gesture timing
            if letter_start_time is not None:
                hold_time = time.time() - letter_start_time
                if hold_time < LETTER_HOLD_THRESHOLD:
                    progress = int((hold_time / LETTER_HOLD_THRESHOLD) * 100)
                    cv2.putText(frame, f"Hold: {progress}%", (x1, y2 + 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

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
    else:
        # Reset all states when no hand is detected
        predicted_character = 'None'
        current_letter = None
        current_prediction = None
        letter_start_time = None
        dnb_start_time = None
        if is_playing:
            dnb_song.stop()
            is_playing = False

    # Display recording status and current/completed sentences
    display_y = 30  # Starting y position for text

    # Display current sentence being recorded
    if is_recording:
        if current_sentence:  # Only display if there are letters
            current_text = "Recording: " + ' '.join(current_sentence)
            print(f"Current sentence: {current_text}")  # Debug print
        else:
            current_text = "Recording: (empty)"
        cv2.putText(frame, current_text, (10, display_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Display previous sentence
    if sentences:
        last_text = "Last: " + ' '.join(sentences[-1])
        cv2.putText(frame, last_text, (10, display_y + 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    
    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        if not is_recording:
            # Start recording new sentence
            is_recording = True
            current_sentence = []
        else:
            # Finish recording and save sentence
            is_recording = False
            if current_sentence:  # Only add if not empty
                sentences.append(current_sentence.copy())
                print(f"Recorded sentence: {' '.join(current_sentence)}")
                text = google_tr.translate_text(' '.join(current_sentence), 'en', 'ko')
                google_tr.speak_text(text, target_lanz='ko')

    elif key == ord('b') and is_recording:
        if current_sentence:
            current_sentence.pop()
    
# Make sure to stop the song when quitting
if is_playing:
    dnb_song.stop()
cap.release()
cv2.destroyAllWindows()