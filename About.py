import dash_bootstrap_components as dbc
from dash import *


about = html.Div([
    html.Div([html.Br()], className=''),
    dbc.Container([
        dbc.Card([
            dbc.CardBody([
                html.P('The following is a final year project made by BCA students'),
                html.P('Mohammad Shariq Saifi'),
                html.P('Akash Kumar Yadav'),
                html.P('It is a Dashboard which is to be used for visualization for data regarding food production, food supply, food wastage, food categories and countries affiliated.'),
                html.Hr(),
                html.Div([
                    html.A([
                        html.Button(['Home'], className = 'btn-dark')
                    ], href='/')
                ], className='col auto text-center ')
            ])
        ])
    ])
], className='row text-center auto card-title')