import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load the dataset
data = pd.read_csv('./indian_celebrity_dataset.csv')

# Preprocess the categorical features
categorical_features = ['Gender', 'Body Type', 'Face Shape', 'Skin Tone']
encoders = {}  # To store encoders for later use

for feature in categorical_features:
    encoder = LabelEncoder()
    data[feature] = encoder.fit_transform(data[feature])
    encoders[feature] = encoder  # Store the encoder for future inverse transforms if needed

# Normalize the height and weight
scaler = StandardScaler()
data[['Height (cm)', 'Weight (kg)']] = scaler.fit_transform(data[['Height (cm)', 'Weight (kg)']])

# Features and target
X = data.drop(columns=['Name', 'Age', 'Dressing Style','Favorite Fashion Colors 1', 'Favorite Fashion Colors 2', 'Red Carpet Outfits 1', 'Red Carpet Outfits 2'])
y = data['Name']

# Train the KNN model
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

def recommendCelebrity(input_data):
    # Encode the input attributes
    for feature in categorical_features:
        input_data[feature] = encoders[feature].transform([input_data[feature]])[0]

    # Normalize height and weight for the input data
    input_data['Height (cm)'], input_data['Weight (kg)'] = scaler.transform([[input_data['Height (cm)'], input_data['Weight (kg)']]])[0]

    # Convert input data into the correct format for prediction
    input_data_formatted = [[input_data[feature] for feature in X.columns]]

    # Filter the data to only include celebrities of the same gender as the input data
    input_gender = input_data['Gender']
    filtered_X = X[data['Gender'] == input_gender]
    filtered_y = y[data['Gender'] == input_gender]

    # Train a new KNN model on the filtered data
    filtered_model = KNeighborsClassifier(n_neighbors=3)
    filtered_model.fit(filtered_X, filtered_y)

    # Predict the best match
    celebrity_match = filtered_model.predict(input_data_formatted)
    return celebrity_match[0]