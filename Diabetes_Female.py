import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import joblib
import numpy as np
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load the trained diabetes model
diabetes_prediction_model = joblib.load("./saved_models/diabetes_model.sav")

diabetes_female = dbc.Container(
    dbc.Card(
        dbc.CardBody([
            html.H2(
                "Diabetes Prediction (Female)",
                className="text-center mt-4 mb-4",
                style={"fontWeight": "bold", "color": "black"}
            ),

            # Input Fields
            dbc.Row([
                dbc.Col(dcc.Input(id="pregnancies", type="number", placeholder="Number of Pregnancies", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="glucose", type="number", placeholder="Glucose Level", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="bloodpressure", type="number", placeholder="Blood Pressure", className="form-control"), md=4),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(dcc.Input(id="skinthickness", type="number", placeholder="Skin Thickness", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="insulin", type="number", placeholder="Insulin Level", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="bmi", type="number", step=0.1, placeholder="BMI", className="form-control"), md=4),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col(dcc.Input(id="dpf", type="number", step=0.01, placeholder="Diabetes Pedigree Function", className="form-control"), md=4),
                dbc.Col(dcc.Input(id="age", type="number", placeholder="Age", className="form-control"), md=4),
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
        State("pregnancies", "value"), State("glucose", "value"), State("bloodpressure", "value"),
        State("skinthickness", "value"), State("insulin", "value"), State("bmi", "value"), 
        State("dpf", "value"), State("age", "value")
    ]
)
def predict(n_clicks, pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, age):
    if n_clicks:
        if None in [pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, age]:
            return "⚠️ Please fill all fields before predicting."

        # Convert inputs to model format
        user_input = np.array([pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, age]).reshape(1, -1)

        # Make prediction
        diabetes_prediction = diabetes_prediction_model.predict(user_input)

        # Interpret result
        if diabetes_prediction[0] == 1:
            return html.Div("⚠️ The person is **diabetic**.", className="alert alert-danger")
        else:
            return html.Div("✅ The person is **not diabetic**.", className="alert alert-success")

    return ""

# Callback function to generate and download the PDF report
@dash.callback(
    Output("download-pdf", "data"),
    Input("download-btn", "n_clicks"),
    [
        State("pregnancies", "value"), State("glucose", "value"), State("bloodpressure", "value"),
        State("skinthickness", "value"), State("insulin", "value"), State("bmi", "value"), 
        State("dpf", "value"), State("age", "value"),
        State("prediction-result", "children")
    ],
    prevent_initial_call=True
)
def download_report(n_clicks, pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, age, prediction_result):
    if None in [pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, age, prediction_result]:
        return None

    # Extract text from Dash component
    if isinstance(prediction_result, dict) and "props" in prediction_result:
        prediction_text = prediction_result["props"].get("children", "Prediction not available")
    else:
        prediction_text = "Prediction not available"

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    
    pdf.drawString(100, 750, "Diabetes Prediction Report")
    pdf.line(100, 745, 500, 745)

    data = [
        ("Pregnancies", pregnancies),
        ("Glucose Level", glucose),
        ("Blood Pressure", bloodpressure),
        ("Skin Thickness", skinthickness),
        ("Insulin Level", insulin),
        ("BMI", bmi),
        ("Diabetes Pedigree Function", dpf),
        ("Age", age),
    ]

    y_position = 720
    for label, value in data:
        pdf.drawString(100, y_position, f"{label}: {value}")
        y_position -= 20

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position - 20, f"Prediction Result: {prediction_text}")

    pdf.save()
    buffer.seek(0)

    return dcc.send_bytes(buffer.getvalue(), filename="Diabetes_Report.pdf")
