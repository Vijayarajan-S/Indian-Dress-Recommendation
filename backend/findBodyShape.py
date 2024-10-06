import os
from keras.models import load_model
from keras.preprocessing import image
import numpy as np


# Load the trained model
bodyshapemodel = load_model('./modals/body_shape_model.h5')

def load_and_preprocess_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(128, 128))  # Resize to match training size
        img_array = image.img_to_array(img) / 255.0  # Normalize
        return np.expand_dims(img_array, axis=0)  # Add batch dimension
    except OSError as e:
        print(f"Error loading image {img_path}: {e}")
        return None

def predict_body_shape(img_path):
    img_array = load_and_preprocess_image(img_path)
    if img_array is None:
        print("Image could not be loaded, skipping prediction.")
        return None
    
    predictions = bodyshapemodel.predict(img_array)
    class_names = ['Hourglass', 'Rectangle', 'Inverted Triangle', 'Pear-shaped']
    predicted_class = class_names[np.argmax(predictions)]
    return predicted_class

 