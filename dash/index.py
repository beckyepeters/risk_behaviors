from app import app
from app import server
import matplotlib.pyplot as plt
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import seaborn as sns
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import joblib
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score

colors = ['#b166eb', '#8858D4', '#664CC1', '#4B43B2', '#072B8B']
threshold = 0.413
df = pd.read_csv('data/sex.csv')

app.layout = html.Div(
    children=[
        html.H1(children='Predicting Youth Risk Behavior'),

    html.Div(children='''
Helping parents and professionals have timely and relevant discussions with youth.    
'''),
        dcc.Graph(
        figure={
            'df': [
                {
                    'x': df['year'], 
                    'type': 'hist',
                },
            ],
            'layout': {'title': 'Number of Surveys by Year'},
        },
        ),
        dcc.Graph(
            figure={
                'df': [
                    {
                        'x': df['age'], 
                        'type': 'hist', 
                    },
                ],
                'layout': {'title': 'Age of Participants'},
            },
        ),
        
        ]
    )

# def scores(test_set): 
#     pred_prob = model.predict_proba(test_set)
#     predicted = (pred_prob[:, 1] >= threshold).astype('int')
#     accuracy = metrics.accuracy_score(y_test, predicted)
#     recall = metrics.recall_score(y_test, predicted)
#     precision = metrics.precision_score(y_test, predicted)
#     f1 = metrics.f1_score(y_test, predicted)
#     return accuracy, precision, recall, f1

# def new_event_prediction(event_array): 
#     if event_array is not None and event_array is not '': 
#         try: 
#             pred_prob = model.predict_proba(event_array)
#             predicted = (pred_prob[:, 1] >= threshold).astype('int')
#             if predicted == 1: 
#                 return f'POTENTIAL FRAUD'
#             elif predicted == 0: 
#                 return f'MOST LIKELY LEGITIMATE'
#         except: 
#             pass

@app.callback(
    Output('collapse', 'is_open'), 
    [Input('collapse-button', 'n_clicks')],
    [State('collapse', 'is_open')],
)

# @app.callback(
#     Output(component_id='result', component_property='children'),
#     [Input(component_id='event_array', component_property='value')])


