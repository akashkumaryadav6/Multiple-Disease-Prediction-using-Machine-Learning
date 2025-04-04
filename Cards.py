import dash_bootstrap_components as dbc
from dash import html

# Reusable function for card creation
def create_card(title, image_path, link):
    return dbc.Col(
        html.A(
            dbc.Card(
                [
                    dbc.CardImg(src=image_path, top=True, style={"opacity": 0.4, "width": "80%"}),
                    dbc.CardImgOverlay(
                        dbc.CardBody([html.H4(title, className="card-title text-center")])
                    ),
                ],
                className="shadow"
            ),
            href=link,
            className='nav'
        ),
        xs=12, sm=6, md=4, lg=4, xl=4, className="d-flex justify-content-center align-items-center"
    )

cards = dbc.Container(
    dbc.Row(
        [
            create_card("Heart Disease Prediction", "/static/Images/heart.png", "/heart"),
            create_card("Diabetes in Females Prediction", "/static/Images/diabetes.jpg", "/diabetes_female"),
            create_card("Parkinson's Disease Prediction", "/static/Images/parkinsons.jpg", "/parkinsons"),
            create_card("Diabetes Prediction", "/static/Images/diabetes.jpg", "/diabetes"),
        ],
        className="justify-content-center align-items-center g-4",
    ),
    fluid=True,
    style={"display": "flex", "justify-content": "center", "alignItems": "center", "height": "auto"}
)
