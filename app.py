import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(data_dict, prediction_result):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 40, "Disease Prediction Report")

    c.setFont("Helvetica", 12)
    y = height - 80
    for key, value in data_dict.items():
        c.drawString(30, y, f"{key}: {value}")
        y -= 15
        if y < 40: 
            c.showPage()
            y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, y - 20, f"Prediction Result: {prediction_result}")
    c.save()
    buffer.seek(0)
    return buffer

# Set Streamlit page configuration
st.set_page_config(page_title="Disease Prediction", layout="centered")

# Paths to model files
MODEL_PATHS = {
    "Diabetes": ".\models\diabetes_prediction_model.sav",
    "Heart Disease": ".\models\heart_disease_model.sav",
    "Kidney Disease": ".\models\kidney_disease_model.sav"
}

# Feature templates (based on datasets)
FEATURES = {
    "Diabetes": ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history',
       'bmi', 'HbA1c_level', 'blood_glucose_level'],
    
    "Heart Disease": ['Sex', 'GeneralHealth', 'PhysicalActivities', 'SleepHours',
                 'HadAngina', 'HadStroke', 'HadAsthma',
                 'HadSkinCancer', 'HadCOPD', 'HadDepressiveDisorder', 'HadKidneyDisease',
                 'HadArthritis', 'HadDiabetes', 'DeafOrHardOfHearing',
                 'BlindOrVisionDifficulty', 'DifficultyConcentrating',
                 'DifficultyWalking', 'DifficultyDressingBathing', 'DifficultyErrands',
                 'SmokerStatus', 'ChestScan', 'HeightInMeters', 'WeightInKilograms',
                 'BMI', 'AlcoholDrinkers', 'HIVTesting', 'HighRiskLastYear'],
    "Kidney Disease": ['Age of the patient', 'Blood pressure (mm/Hg)', 'Specific gravity of urine', 'Albumin in urine', 'Sugar in urine',
                 'Red blood cells in urine', 'Pus cells in urine', 'Pus cell clumps in urine', 'Bacteria in urine',
                 'Random blood glucose level (mg/dl)', 'Blood urea (mg/dl)', 'Serum creatinine (mg/dl)', 'Sodium level (mEq/L)',
                 'Potassium level (mEq/L)', 'Hemoglobin level (gms)', 'Packed cell volume (%)', 'White blood cell count (cells/cumm)',
                 'Red blood cell count (millions/cumm)', 'Hypertension (yes/no)', 'Diabetes mellitus (yes/no)', 'Coronary artery disease (yes/no)',
                 'Appetite (good/poor)', 'Anemia (yes/no)', 'Estimated Glomerular Filtration Rate (eGFR)',
                 'Urine protein-to-creatinine ratio', 'Urine output (ml/day)', 'Serum albumin level', 'Cholesterol level',
                 'Parathyroid hormone (PTH) level', 'Serum calcium level', 'Serum phosphate level', 'Family history of chronic kidney disease',
                 'Smoking status', 'Body Mass Index (BMI)', 'Physical activity level', 'Duration of diabetes mellitus (years)', 
                 'Duration of hypertension (years)', 'Cystatin C level', 'Urinary sediment microscopy results', 'C-reactive protein (CRP) level',
                 'Interleukin-6 (IL-6) level']
}

# UI setup
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Disease Prediction App 🩺</h1>", unsafe_allow_html=True)
st.write("Select a disease model and input patient information to predict the condition.")

# Disease model selector
disease = st.selectbox("\U0001F489 Choose Disease Model", list(MODEL_PATHS.keys()))

# Load model
model_path = MODEL_PATHS[disease]
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error(f"Model file for {disease} not found at {model_path}.")
    st.stop()

# User input form
st.subheader(f"\U0001F4DD Enter Patient Data for {disease}")
input_data = {}
with st.form("prediction_form"):
    for feature in FEATURES[disease]:
        val = st.text_input(f"{feature}")
        input_data[feature] = val
    submitted = st.form_submit_button("Predict")

prediction = ''
# Perform prediction
if submitted:
    try:
        input_df = pd.DataFrame([input_data])
        input_df = input_df.astype(float)
        prediction = model.predict(input_df)[0]
        st.success(f"\U00002705 Prediction Result: {prediction}")
    except ValueError as e:
        st.error(f"❌ Invalid input. Please enter all values correctly.\n{e}")

pdf_buffer = create_pdf(input_data, prediction)

st.download_button(
    label="📄 Download Report as PDF",
    data=pdf_buffer,
    file_name=f"{disease}_prediction_report.pdf",
    mime="application/pdf"
)