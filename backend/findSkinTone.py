import cv2
import numpy as np
from mtcnn import MTCNN
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Function to preprocess the skin region for better accuracy
def preprocess_skin_region(roi):
    roi_lab = cv2.cvtColor(roi, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(roi_lab)
    l = cv2.equalizeHist(l)  # Histogram equalization to enhance brightness
    roi_lab = cv2.merge((l, a, b))
    return roi_lab

# Function to enhance contrast of the image
def enhance_image_contrast(img_rgb):
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)  # Applying CLAHE to the L-channel
    lab_clahe = cv2.merge((l_clahe, a, b))
    img_clahe_rgb = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2RGB)
    return img_clahe_rgb

# Function to extract skin region and calculate skin tone histogram features
def extract_skin_histogram(roi):
    roi_lab = cv2.cvtColor(roi, cv2.COLOR_RGB2LAB)
    hist_lab = [cv2.calcHist([roi_lab], [i], None, [8], [0, 256]) for i in range(3)]
    hist_features = np.concatenate([h.flatten() for h in hist_lab])
    return hist_features

# Function to detect skin tone from an image using RandomForestClassifier
def detect_skin_tone(image_path, model):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to load image {image_path}")
        return None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = enhance_image_contrast(img_rgb)

    # Detect faces using MTCNN
    faces = detector.detect_faces(img_rgb)

    if len(faces) == 0:
        print("No faces detected.")
        return None

    # Extract the first detected face
    face = faces[0]
    x, y, w, h = face['box']

    # Define a region of interest (ROI) around the face
    roi = img_rgb[y:y + h, x:x + w]  # Use the entire face for better context

    # Preprocess and extract histogram features
    roi_lab = preprocess_skin_region(roi)
    hist_features = extract_skin_histogram(roi_lab)

    # Normalize features
    hist_features = hist_features / np.linalg.norm(hist_features)

    # Predict skin tone using the pre-trained model
    predicted_skin_tone = model.predict([hist_features])
    return predicted_skin_tone[0]

# Function to train a RandomForest model
def train_skin_tone_classifier(data_dir):
    X_train = []
    y_train = []

    # Loop through each file in the directory
    for filename in os.listdir(data_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Add other image formats as needed
            img_path = os.path.join(data_dir, filename)
            img = cv2.imread(img_path)
            if img is not None:
                skin_tone = determine_skin_tone_from_filename(filename)  # Implement this function
                hist_features = extract_skin_histogram(img)
                
                # Append features and labels
                X_train.append(hist_features)
                y_train.append(skin_tone)
            else:
                print(f"Warning: Unable to load image {img_path}")

    if len(X_train) == 0:
        print("No valid training data found.")
        return None
    
    # Convert to numpy arrays
    X_train = np.array(X_train)
    y_train = np.array(y_train)

    # Train a RandomForest classifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # Save the model for future use
    joblib.dump(rf, 'skin_tone_rf_model.pkl')
    print("RandomForest model trained and saved.")
    return rf

# Function to determine skin tone from filename
def determine_skin_tone_from_filename(filename):
    if "fair" in filename.lower():
        return 'Fair'
    elif "medium" in filename.lower():
        return 'Medium'
    elif "dark" in filename.lower():
        return 'Dark'
    else:
        return 'Unknown'

# Load pre-trained model from joblib
def load_model(model_path):
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print("Model loaded successfully.")
        return model
    else:
        print(f"Error: Model file not found at {model_path}")
        return None


# Load MTCNN face detector
detector = MTCNN()
model_path = './modals/skin_tone_rf_model.pkl'  # Path to the pre-trained RandomForest model
model = load_model(model_path)


def findSkinToneFunction(image_path):
    # Detect and print the skin tone
    skin_tone = detect_skin_tone(image_path, model)
    if skin_tone:
        return skin_tone
    else:
        return "none"