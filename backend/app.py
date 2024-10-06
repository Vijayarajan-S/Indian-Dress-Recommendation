from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os
import pandas as pd
from werkzeug.utils import secure_filename

# Import your functions
from getCelebrity import recommendCelebrity
from findFaceShape import detect_face_shape
from findBodyShape import predict_body_shape
from findSkinTone import findSkinToneFunction

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['thuli']
collection = db['Users']

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'  # Change this to your desired directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/userData', methods=['POST'])
def submit_data():
    # Get data from AJAX request
    data = request.get_json()
    name = data.get('name')
    gender = data.get('gender')
    email = data.get('email')
    age = data.get('age')
    height = data.get('height')
    weight = data.get('weight')
    
    try:
        # Insert into MongoDB
        user_info = {
            "email": email,
            "name": name,
            "gender": gender,
            "age": age,
            "height": height,
            "weight": weight
        }
        result = collection.insert_one(user_info)
        
        return jsonify({"message": "Data inserted successfully!", "id": str(result.inserted_id)})
    except Exception as e:
        return jsonify({"message": "Data not inserted!", "error": str(e)}), 500


@app.route('/getCelebrityData', methods=['POST'])
def get_celebrity():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    # Accessing the other fields from the form data
    emailId = request.form.get('email')  # Use request.form to get non-file fields
    theme_want = request.form.get('preference')

    if not emailId:
        return jsonify({"error": "Email ID is required"}), 400

    # If the user does not select a file
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file to the upload folder
    if file:
        # Create a secure filename and save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        user = collection.find_one({"email": emailId})
        if not user:
            return jsonify({"error": "User not found!"}), 404

        skin_tone = findSkinToneFunction(file_path)  # Pass the full path to your function
        body_type = predict_body_shape(file_path)
        face_shape = detect_face_shape(file_path)

        input_data = {
            'Gender': user["gender"],
            'Body Type': body_type,
            'Face Shape': face_shape,
            'Skin Tone': skin_tone,
            'Height (cm)': user["height"],
            'Weight (kg)': user["weight"]
        }

        print("--------------------")
        print(input_data)
        print("--------------------")

        dress_data = pd.read_csv("./dress_dataset.csv")
        predicted_celebrity = recommendCelebrity(input_data)

        # Filter dress dataset based on the predicted celebrity and occasion
        dress_recommendation = dress_data[
            (dress_data['Celebrity Name'] == predicted_celebrity) &
            (dress_data['Costume Theme'] == theme_want)  # Replace with relevant occasion if known
        ]

        if dress_recommendation.empty:
            return jsonify({"celebrity" : predicted_celebrity,"message": "No dress recommendations found."}), 200

        return jsonify({"message": "Dress recommendations retrieved successfully!", "data": dress_recommendation.to_dict(orient='records')}), 200

    return jsonify({"message": "Error during file processing."}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8888)
