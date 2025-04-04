import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, callback
from Cards import cards
from Heart import heart
# from Diabetes_Female import diabetes_female
from Navbar import navbar

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.1.0/mdb.min.css'], 
                suppress_callback_exceptions=True, title="Disease Prediction using Patient Data")

server = app.server

app.layout = html.Div([dcc.Location(id="url", refresh=True), navbar, 
html.Div([], id="page-content", className="pt-5")])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)

def pages(pathname):
    if pathname == '/':
        return cards
    elif pathname == '/heart':
        return heart
    # elif pathname == '/diabetes_female':
    #     return diabetes_female
    else:
        return cards

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)