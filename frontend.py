import streamlit as st
import requests

import app

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide"
)

# Sidebar
st.sidebar.title("🩺 Diabetes Prediction")
st.sidebar.markdown("""
### About
This application predicts whether a patient is diabetic based on medical parameters.

### Features
- ANN Model
- Flask Backend API
- Streamlit Frontend
- Probability Score
- Real-time Prediction

### Developer
Durgesh Singh
""")

# Title
st.title("🩺 Diabetes Prediction System")
st.markdown("""
This application uses an Artificial Neural Network (ANN) to predict whether a person is diabetic.
Enter the patient details below and click **Predict**.
""")

# Input columns
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("Pregnancies", min_value=0, value=6)
    glucose = st.number_input("Glucose Level", min_value=0, value=148)
    blood_pressure = st.number_input("Blood Pressure", min_value=0, value=72)
    skin_thickness = st.number_input("Skin Thickness", min_value=0, value=35)

with col2:
    insulin = st.number_input("Insulin", min_value=0, value=0)
    bmi = st.number_input("BMI", min_value=0.0, value=33.6)
    diabetes_pedigree = st.number_input(
        "Diabetes Pedigree Function",
        min_value=0.0,
        value=0.627,
        format="%.3f"
    )
    age = st.number_input("Age", min_value=1, value=50)

# BMI Status
if bmi < 18.5:
    st.info("BMI Category: Underweight")
elif bmi < 25:
    st.success("BMI Category: Normal")
elif bmi < 30:
    st.warning("BMI Category: Overweight")
else:
    st.error("BMI Category: Obese")

# Predict button
if st.button("🔍 Predict Diabetes"):

    data = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": diabetes_pedigree,
        "Age": age
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json=data
        )

        result = response.json()

        prediction = result["prediction"]
        probability = result["probability"]

        st.subheader("Prediction Result")

        if prediction == 1:
            st.error("⚠️ High Risk of Diabetes")
        else:
            st.success("✅ Low Risk of Diabetes")

        st.metric("Prediction Probability", f"{probability*100:.2f}%")

    except:
        st.error("Unable to connect to Flask API.")

# Divider
st.divider()

# Dataset Information
st.subheader("📊 Features Used")

st.markdown("""
| Feature | Description |
|-----------|-------------|
| Pregnancies | Number of pregnancies |
| Glucose | Plasma glucose concentration |
| BloodPressure | Diastolic blood pressure |
| SkinThickness | Triceps skin fold thickness |
| Insulin | 2-Hour serum insulin |
| BMI | Body Mass Index |
| DiabetesPedigreeFunction | Diabetes pedigree function |
| Age | Age of patient |
""")

# Footer
st.divider()
st.caption("Built with TensorFlow • Flask • Streamlit")

