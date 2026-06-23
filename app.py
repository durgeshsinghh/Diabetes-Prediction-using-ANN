from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load trained model
model = load_model('best_model.keras')

@app.route('/')
def home():
    return "Diabetes Prediction API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data
        data = request.get_json()

        # Extract features
        features = np.array([
            data['Pregnancies'],
            data['Glucose'],
            data['BloodPressure'],
            data['SkinThickness'],
            data['Insulin'],
            data['BMI'],
            data['DiabetesPedigreeFunction'],
            data['Age']
        ]).reshape(1, -1)

        # Prediction probability
        probability = model.predict(features)[0][0]

        # Class prediction
        prediction = int(probability >= 0.5)

        return jsonify({
            'prediction': prediction,
            'probability': float(probability)
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)