import os
import cv2
import dlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# Path to the shape predictor model file
model_path = './modals/shape_predictor_68_face_landmarks.dat'

# Load dlib's face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(model_path)

# Train the face shape classifier
def train_face_shape_classifier():
    # Example training data: 100 samples, 4 features (random for now)
    X_train = np.random.rand(100, 4)  # 4 features from facial ratios
    Y_train = np.random.choice(['Oval', 'Square', 'Round', 'Heart'], 100)  # Random labels for now 
    classifier = RandomForestClassifier(n_estimators=100)
    classifier.fit(X_train, Y_train)
    return classifier

classifier = train_face_shape_classifier()

# Function to convert dlib shape to numpy array
def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords

# Function to calculate face geometric features from 68 landmarks
def calculate_face_features(landmarks):
    left_eye = np.mean(landmarks[36:42], axis=0)  # Average of left eye points
    right_eye = np.mean(landmarks[42:48], axis=0)  # Average of right eye points
    nose = landmarks[30]  # Nose tip
    jaw_width = np.linalg.norm(landmarks[3] - landmarks[13])  # Jawline width between points 4 and 12
    cheekbone_width = np.linalg.norm(landmarks[1] - landmarks[15])  # Cheekbone width
    face_height = np.linalg.norm(landmarks[8] - (left_eye + right_eye) / 2)  # Approx face height

    # Calculate ratios and angles
    eye_distance = np.linalg.norm(left_eye - right_eye)
    mouth_width = np.linalg.norm(landmarks[48] - landmarks[54])
    
    eye_to_face_ratio = eye_distance / face_height
    mouth_to_face_ratio = mouth_width / face_height
    jaw_to_face_ratio = jaw_width / face_height
    cheekbone_to_face_ratio = cheekbone_width / face_height

    return np.array([eye_to_face_ratio, mouth_to_face_ratio, jaw_to_face_ratio, cheekbone_to_face_ratio])

# Classify face shape based on features
def classify_face_shape(features, classifier):
    features = features.reshape(1, -1)
    predicted_face_shape = classifier.predict(features)[0]
    return predicted_face_shape

# Detect face shape from image
def detect_face_shape(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(gray, 1)

    if len(faces) == 0:
        print("No faces detected.")
        return None

    for rect in faces:
        shape = predictor(gray, rect)
        landmarks = shape_to_np(shape)

        # Draw landmarks and face box
        for (x, y) in landmarks:
            cv2.circle(img, (x, y), 2, (0, 255, 0), -1)

        features = calculate_face_features(landmarks)
        face_shape = classify_face_shape(features, classifier)

    return face_shape
