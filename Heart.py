import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import joblib
import numpy as np
import base64
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load the trained model
heart_disease_model = joblib.load("./saved_models/heart_disease_model.sav")

heart = dbc.Container(
    dbc.Card(
        dbc.CardBody([
            html.H2(
                "Heart Disease Prediction",
                className="text-center mt-4 mb-4",
                style={"fontWeight": "bold", "color": "black"}
            ),

            # Input Fields
            dbc.Row([
                dbc.Col(dcc.Input(id="age", type="number", placeholder="Age", className="form-control"), md=4),
                dbc.Col(dcc.Dropdown(id="sex", options=[{"label": "Male", "value": 1}, {"label": "Female", "value": 0}], placeholder="Sex"), md=4),
                dbc.Col(dcc.Input(id="cp", type="number", placeholder="Chest Pain Type", className="form-control"), md=4),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(dcc.Input(id="trestbps", type="number", placeholder="Resting Blood Pressure", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="chol", type="number", placeholder="Cholesterol", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="fbs", type="number", placeholder="Fasting Blood Sugar (1=True, 0=False)", className="form-control"), md=4),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(dcc.Input(id="restecg", type="number", placeholder="Resting ECG", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="thalach", type="number", placeholder="Max Heart Rate", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="exang", type="number", placeholder="Exercise Induced Angina (1/0)", className="form-control"), md=4),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(dcc.Input(id="oldpeak", type="number", step=0.1, placeholder="ST Depression", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="slope", type="number", placeholder="Slope", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="ca", type="number", placeholder="Number of Major Vessels", className="form-control"), md=4),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(dcc.Input(id="thal", type="number", placeholder="Thalassemia Type", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="name", type="text", placeholder="Name", className="form-control"), md=4),
            ], className="mb-3"),

            # Buttons for Prediction & Download
            dbc.Row([
                dbc.Col(dbc.Button("Get Prediction", id="predict-btn", color="primary", className="mt-3"), md=6),
                dbc.Col(dbc.Button("Download Report", id="download-btn", color="success", className="mt-3"), md=6),
            ], className="mb-3"),

            # Output Display
            html.Div(id="prediction-result", className="mt-4 text-center"),

            # Hidden link for downloading the PDF
            dcc.Download(id="download-pdf")
        ]),
        className="shadow p-4",  # Adds shadow and padding for styling
        style={"borderRadius": "15px", "maxWidth": "800px", "marginTop":"25%"}  # Rounded corners & width control
    ),
    fluid=True,
    className="d-flex flex-column justify-content-center align-items-center"
)

# Callback function for prediction
@dash.callback(
    Output("prediction-result", "children"),
    Input("predict-btn", "n_clicks"),
    [
        State("age", "value"), State("sex", "value"), State("cp", "value"),
        State("trestbps", "value"), State("chol", "value"), State("fbs", "value"),
        State("restecg", "value"), State("thalach", "value"), State("exang", "value"), State("oldpeak", "value"),
         State("slope", "value"), State("ca", "value"), State("thal", "value"), State("name", "value")
    ]
)
def predict(n_clicks, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, name):
    if n_clicks:
        if None in [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, name]:
            return "⚠️ Please fill all fields before predicting."

        # Convert inputs to model format
        user_input = np.array([age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]).reshape(1, -1)

        # Make prediction
        heart_prediction = heart_disease_model.predict(user_input)

        # Interpret result
        if heart_prediction[0] == 1:
            return html.Div(f"🩺 {name} **HAS** heart disease!", className="alert alert-danger")
        else:
            return html.Div(f"✅ {name} **does NOT have** heart disease.", className="alert alert-success")

    return ""

# Callback function to generate and download the PDF report
@dash.callback(
    Output("download-pdf", "data"),
    Input("download-btn", "n_clicks"),
    [
        State("age", "value"), State("sex", "value"), State("cp", "value"),
        State("trestbps", "value"), State("chol", "value"), State("fbs", "value"),
        State("restecg", "value"), State("thalach", "value"), State("exang", "value"), State("oldpeak", "value"), 
        State("slope", "value"), State("ca", "value"), State("thal", "value"), State("name", "value"),
        State("prediction-result", "children")
    ],
    prevent_initial_call=True
)
def download_report(n_clicks, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, name, prediction_result):
    if None in [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, name, prediction_result]:
        return None

    # Extract text from Dash component
    if isinstance(prediction_result, dict) and "props" in prediction_result:
        prediction_text = prediction_result["props"].get("children", "Prediction not available")
    else:
        prediction_text = "Prediction not available"

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    
    pdf.drawString(100, 750, "Heart Disease Prediction Report")
    pdf.line(100, 745, 500, 745)

    data = [
        ("Name", name),
        ("Age", age),
        ("Sex", "Male" if sex == 1 else "Female"),
        ("Chest Pain Type", cp),
        ("Resting Blood Pressure", trestbps),
        ("Cholesterol", chol),
        ("Fasting Blood Sugar", "High" if fbs == 1 else "Normal"),
        ("Resting ECG", restecg),
        ("Max Heart Rate", thalach),
        ("Exercise Induced Angina", "Yes" if exang == 1 else "No"),
        ("ST Depression", oldpeak),
        ("Slope", slope),
        ("Major Vessels", ca),
        ("Thalassemia Type", thal),
    ]

    y_position = 720
    for label, value in data:
        pdf.drawString(100, y_position, f"{label}: {value}")
        y_position -= 20

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position - 20, f"Prediction Result: {prediction_text}")

    pdf.save()
    buffer.seek(0)

    return dcc.send_bytes(buffer.getvalue(), filename="Heart_Disease_Report.pdf")

