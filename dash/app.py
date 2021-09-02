import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

df = pd.read_csv('data/sex.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
age = ['12 yrs -', '13 yrs', '14 yrs', '15 yrs', '16 yrs', '17 yrs', '18 yrs +']
age_dict = {'12 yrs -': 1, '13 yrs': 2, '14 yrs': 3, 
           '15 yrs': 4, '16 yrs': 5, '17 yrs': 6, '18 yrs +': 7}
sex = ['Female', 'Male']
sex_dict = {'Female': 1, 'Male': 2}
race7 = ['Hisp/Latinx', 'Black or Af Am', 
               'White', 'Asian', 'Multiple Races', 
               'NatHaw/OtherPacIsl', 'AmInd/AlaskaNat']
race7_dict = {'AmInd/AlaskaNat': 1, 'Asian': 2, 'Black or Af Am': 3, 
             'Hisp/Latinx': 4, 'NatHaw/OtherPacIsl': 5, 'White': 6, 'Multiple Races (Non-Hisp)': 7}
bmi = ['Below 18.5', '18.5-24.9', '25.0-29.9', '30.0 and Above']
bmi_dict = {'Below 18.5': 18.5, '18.5-24.9': 20, '25.0-29.9': 27.5, '30.0 and Above': 30}
grade = ['9th Grade', '10th Grade', '11th Grade', '12th Grade']
grade_dict = {'9th Grade': 1, '10th Grade': 2, '11th Grade': 3, 
             '12th Grade': 4}
sexid2 = ['Heterosexual', 'Sexual Minority', 'Unsure']
sexid2_dict = {'Heterosexual': 1, 'Sexual Minority': 2, 'Unsure': 3}
model = joblib.load('rf_hyp.sav')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Modeling the Youth Risk Behavior Survey, 2009-2019'
server = app.server

fig = px.histogram(data_frame=df, x=df['year'], color='sex', 
    barmode='group', range_x=[2009, 2019], color_discrete_sequence=['#b166eb', '#8858D4', '#664CC1', '#4B43B2', '#072B8B'])

series_names = ["Female", "Male"]

for idx, name in enumerate(series_names):
    fig.data[idx].name = name
    fig.data[idx].hovertemplate = name
fig.update_layout(
    xaxis=dict(tickmode='linear', tick0=2009, dtick=2),
    title='Figure 1: Number of Completed Surveys by Year',
    xaxis_title="Year",
    yaxis_title="Count",
    legend_title="Gender Assigned at Birth"
    )

app.layout = html.Div(
    children=[
        html.H1(children='Predicting Youth Risk Behavior'),

    html.Div(children='''
Helping parents and professionals have relevant discussions with youth.    
'''),
            dbc.Button(
            "About the Youth Risk Behavior Survey", 
            style={'backgroundColor': '#b166eb', 
                'color':'white',
                'border':'1.5px black solid', 
                'height': '50px',
                'text-align':'center', 
                'marginTop': 30},
            block=True, 
            id="collapse-button", 
            className = "mr-1", 
            color="primary", 
            n_clicks=0
        ),
        dbc.Collapse(
            dbc.Card(dcc.Markdown('''
The [Centers for Disease Control and Prevention](https://www.cdc.gov/) (CDC) 
supports health care providers, parents, teachers, and other adults with 
data from their Youth Risk Behavior Survey (YRBS), a biannual survey conducted across the nation since 1999. 
The YRBS (conducted by the CDC, state, territorial, and local education and health agencies and tribal governments) 
surveys youth from across the country about health-related behaviors that contribute to leading causes of death and 
disability among youth and adults, including (listed from [the YRBSS website](https://www.cdc.gov/healthyyouth/data/yrbs/index.htm)): 
* Behaviors that contribute to unintentional injuries and violence
* Sexual behaviors related to unintended pregnancy and sexually transmitted diseases 
* Alcohol and other drug use
* Tobacco use
* Unhealthy dietary behaviors
* Inadequate physical activity''')),
            id="collapse", 
            is_open=False, 
        ),
        dbc.Button(
            "About this Dashboard and Project", 
            style={'backgroundColor': '#664CC1', 
                'color':'white',
                'border':'1.5px black solid', 
                'height': '50px',
                'text-align':'center', 
                'marginTop': 30},
            block=True, 
            id="collapse-button-2", 
            className = "mr-1", 
            color="success", 
            n_clicks=0
        ),
        dbc.Collapse(
            dbc.Card(dcc.Markdown('''
This dashboard uses data from the YRBS from 2009-2019. Using a machine learning classification 
algorithm (Random Forest), the dashboard provides probabilities that an individual 
has engaged in a risk behavior.''')),
            id="collapse-2", 
            is_open=False, 
        ),
        dbc.Button(
            "Important Considerations", 
            style={'backgroundColor': '#072B8B', 
                'color':'white',
                'border':'1.5px black solid', 
                'height': '50px',
                'text-align':'center', 
                'marginTop': 30, 
                'marginBottom': 30},
            block=True, 
            id="collapse-button-3", 
            className = "mr-1", 
            color="info", 
            n_clicks=0
        ),
        dbc.Collapse(
            dbc.Card(dcc.Markdown('''
Important Considerations
* Insights over Answers:
    * Certainly a high probability of a person engaging in an activity does not mean that the individual has indeed made that choice.
* Discussions over Discipline:
    * The hope is that adult knowledge of the prevalence of these risk behaviors will lead to more appropriate, 
    relevant conversations with young people about their own health, not punish them with information.
* Reality over Determinism:
    * Even if the model were 100 percent accurate, actual choices are impossible to predict for individual people. 
''')),
            id="collapse-3", 
            is_open=False, 
        ),
    dcc.Tabs([
        dcc.Tab(label='Explore the Data', children=[
            dcc.Graph(
        figure=fig
    )

        ]),
        dcc.Tab(label='Make Predictions', children=[
            dcc.Markdown('''
            Use the dropdown controls to predict youth risk behavior based on age, gender
            assigned at birth, race/ethnicity, age, and grade.'''),
            html.Div(id='prediction-content', style={'fontWeight': 'bold'}),
            html.Div([ 
                dcc.Markdown('##### Age'), 
                dcc.Dropdown(
                    id='age', 
                    options=[{'label': age, 'value': age} for age in age], 
                    value=age[0], 
                    style=dict(width='33%')
                ),
            ], style={'padding': '1.5em'}),
            html.Div([ 
                dcc.Markdown('##### Gender Assigned at Birth'), 
                dcc.Dropdown(
                    id='sex', 
                    options=[{'label': sex, 'value': sex} for sex in sex], 
                    value=sex[0],
                    style=dict(width='33%')
                ),
            ], style={'padding': '1.5em'}),
            
            html.Div([ 
                dcc.Markdown('##### Race / Ethnicity'), 
                dcc.Dropdown(
                    id='race7', 
                    options=[{'label': race7, 'value': race7} for race7 in race7], 
                    value=race7[0],
                    style=dict(width='33%')
                ),
            ], style={'padding': '1.5em'}),

            html.Div([ 
                dcc.Markdown('##### BMI'), 
                dcc.Dropdown(
                    id='bmi', 
                    options=[{'label': bmi, 'value': bmi} for bmi in bmi], 
                    value=bmi[0],
                    style=dict(width='33%')
                ),
            ], style={'padding': '1.5em'}),

            html.Div([ 
                dcc.Markdown('##### Grade'), 
                dcc.Dropdown(
                    id='grade', 
                    options=[{'label': grade, 'value': grade} for grade in grade], 
                    value=grade[0],
                    style=dict(width='33%')
                ),
            ], style={'padding': '1.5em'}),

            html.Div([ 
                dcc.Markdown('##### Sexual Identity'), 
                dcc.Dropdown(
                    id='sexid2', 
                    options=[{'label': sexid2, 'value': sexid2} for sexid2 in sexid2], 
                    value=sexid2[0],
                    style=dict(width='33%')
                ),
            ], style={'padding': '1.5em'}),

            html.Div([
                dcc.Textarea(
                    id='prediction-results-area', 
                    value=f'Your predictions are: '
                ), 
                html.Div(id='predict')
            ]), 
            
], style={'width': '30%', 'display': 'inline-block', 'display': 'flex'},
),

        dcc.Tab(label='Visualize the Connections', children=[
            dcc.Markdown('''The graph network shown below is based on a 
            subsample of 10,000 surveys from the original dataset, maintaining the proportions of target 
            classifications. Each node is a negative risk behavior and the directional edges 
            between the nodes represent the proportion of survey respondents who answered 
            affirmatively to any of those questions. For example, 31.5 percent of respondents who
            reported feeling sad or hopeless for more than 2 weeks in a row also reported getting
            less than 8 hours of sleep on an average school night. This graph may provide some 
            further direction to dashboard users about potentially relevant discussions with youth.
            '''), 
            cyto.Cytoscape(
        id='cytoscape',
        layout={'name': 'circle', 'directed':True},
        style={'width': '80%', 'height': '800px'},
        boxSelectionEnabled=True,
        responsive=True, 
        elements=[
            {'data': {'id': 'Never / Rarely Wear a Seatbelt',
                'value': 'Never / Rarely Wear a Seatbelt',
                'label': 'Never / Rarely Wear a Seatbelt'}, 
                'position': {'x': 75, 'y': 100}},
     {'data': {'id': 'Drink and Drive 30d',
     'value': 'Drink and Drive 30d',
     'label': 'Drink and Drive 30d'}},
   {'data': {'id': 'Carry a Weapon 30d',
     'value': 'Carry a Weapon 30d',
     'label': 'Carry a Weapon 30d'}},
   {'data': {'id': 'Felt Unsafe at School',
     'value': 'Felt Unsafe at School',
     'label': 'Felt Unsafe at School'}},
   {'data': {'id': 'Felt Sad or Hopeless, 2 wks',
     'value': 'Felt Sad or Hopeless, 2 wks',
     'label': 'Felt Sad or Hopeless, 2 wks'},
     'classes': 'interest'},
   {'data': {'id': 'Ever Tried Cigarettes',
     'value': 'Ever Tried Cigarettes',
     'label': 'Ever Tried Cigarettes'}, 
     'classes': 'interest'},
   {'data': {'id': 'Drank Alcohol, 30d',
     'value': 'Drank Alcohol, 30d',
     'label': 'Drank Alcohol, 30d'}},
   {'data': {'id': 'Ever used Marijuana',
     'value': 'Ever used Marijuana',
     'label': 'Ever used Marijuana'}},
   {'data': {'id': 'Ever Had Sex',
     'value': 'Ever Had Sex',
     'label': 'Ever Had Sex'}, 
     'classes': 'interest'},
   {'data': {'id': 'Watch >3h TV on school days',
     'value': 'Watch >3h TV on school days',
     'label': 'Watch >3h TV on school days'}},
   {'data': {'id': 'Get <8h Sleep on Avg School Night',
     'value': 'Get <8h Sleep on Avg School Night',
     'label': 'Get <8h Sleep on Avg School Night'}},
  {'data': {'weight': '0.5%',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Drink and Drive 30d'}},
   {'data': {'weight': '1.0%',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Carry a Weapon 30d'}},
   {'data': {'weight': '1.0%',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Felt Unsafe at School'}},
   {'data': {'weight': '3.0%',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Felt Sad or Hopeless, 2 wks'}},
   {'data': {'weight': '1.5%',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Ever Tried Cigarettes'}},
   {'data': {'weight': '2.1%',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '3.5%',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '3.3%',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '2.0%',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '5.8%',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '0.6%',
     'source': 'Drink and Drive 30d',
     'target': 'Carry a Weapon 30d'}},
   {'data': {'weight': '0.5%',
     'source': 'Drink and Drive 30d',
     'target': 'Felt Unsafe at School'}},
   {'data': {'weight': '1.0%',
     'source': 'Drink and Drive 30d',
     'target': 'Felt Sad or Hopeless, 2 wks'}},
   {'data': {'weight': '1.3%',
     'source': 'Drink and Drive 30d',
     'target': 'Ever Tried Cigarettes'}},
   {'data': {'weight': '2.1%',
     'source': 'Drink and Drive 30d',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '1.9%',
     'source': 'Drink and Drive 30d',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '1.7%',
     'source': 'Drink and Drive 30d',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '0.5%',
     'source': 'Drink and Drive 30d',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '1.8%',
     'source': 'Drink and Drive 30d',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '1.5%',
     'source': 'Carry a Weapon 30d',
     'target': 'Felt Unsafe at School'}},
   {'data': {'weight': '4.4%',
     'source': 'Carry a Weapon 30d',
     'target': 'Felt Sad or Hopeless, 2 wks'}},
   {'data': {'weight': '3.0%',
     'source': 'Carry a Weapon 30d',
     'target': 'Ever Tried Cigarettes'}},
   {'data': {'weight': '4.2%',
     'source': 'Carry a Weapon 30d',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '5.4%',
     'source': 'Carry a Weapon 30d',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '5.0%',
     'source': 'Carry a Weapon 30d',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '2.2%',
     'source': 'Carry a Weapon 30d',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '7.4%',
     'source': 'Carry a Weapon 30d',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '6.0%',
     'source': 'Felt Unsafe at School',
     'target': 'Felt Sad or Hopeless, 2 wks'}},
   {'data': {'weight': '2.3%',
     'source': 'Felt Unsafe at School',
     'target': 'Ever Tried Cigarettes'}},
   {'data': {'weight': '3.4%',
     'source': 'Felt Unsafe at School',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '4.8%',
     'source': 'Felt Unsafe at School',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '4.5%',
     'source': 'Felt Unsafe at School',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '2.5%',
     'source': 'Felt Unsafe at School',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '8.9%',
     'source': 'Felt Unsafe at School',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '8.3%',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Ever Tried Cigarettes'}},
   {'data': {'weight': '11.8%',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '17.9%',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '15.6%',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '8.6%',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '31.5%',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '8.3%',
     'source': 'Ever Tried Cigarettes',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '11.6%',
     'source': 'Ever Tried Cigarettes',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '9.3%',
     'source': 'Ever Tried Cigarettes',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '3.7%',
     'source': 'Ever Tried Cigarettes',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '12.7%',
     'source': 'Ever Tried Cigarettes',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '17.3%',
     'source': 'Drank Alcohol, 30d',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '13.7%',
     'source': 'Drank Alcohol, 30d',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '5.1%',
     'source': 'Drank Alcohol, 30d',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '19.9%',
     'source': 'Drank Alcohol, 30d',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '22.0%',
     'source': 'Ever used Marijuana',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '8.4%',
     'source': 'Ever used Marijuana',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '30.0%',
     'source': 'Ever used Marijuana',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '7.8%',
     'source': 'Ever Had Sex',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '27.5%',
     'source': 'Ever Had Sex',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '16.6%',
     'source': 'Watch >3h TV on school days',
     'target': 'Get <8h Sleep on Avg School Night'}}
], 
stylesheet=[
            {
            'selector': 'node',
            'style': {
                'content': 'data(label)'
            }
        },
            {
                'selector': '.interest', 
                'style': {
                    'background-color': '#664CC1', 
                    'line-color': 'black'
                }
            }, 
            {
            'selector': 'edge',
            'style': {
                'label': 'data(weight)', 
                'curve-style': 'bezier', 
                'target-arrow-shape': 'triangle'
            }},  
            {
            'selector': '#BA',
            'style': {
                'source-arrow-color': '#8858D4', 
                'source-arrow-shape': 'triangle', 
                'line-color': '#8858D4', 
                'arrow-scale': 4
            }},
            {
            'selector': '#DA',
            'style': {
                'target-arrow-color': '#8858D4', 
                'target-arrow-shape': 'triangle', 
                'line-color': '#4B43B2', 
                'arrow-scale': 4
            }}
        ])
        ]
    ),
])
            ])

@app.callback(
    Output("collapse", "is_open"),
              [Input("collapse-button", "n_clicks")],
              [State("collapse", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-2", "is_open"),
              [Input("collapse-button-2", "n_clicks")],
              [State("collapse-2", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-3", "is_open"),
              [Input("collapse-button-3", "n_clicks")],
              [State("collapse-3", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    dash.dependencies.Output('predict', 'children'), 
    [dash.dependencies.Input('age', 'value'), 
    Input('sex', 'value'), 
    Input('race7', 'value'), 
    Input('bmi', 'value'),
    Input('grade', 'value'),
    Input('sexid2', 'value')])
def predict(age, sex, race7, bmi, grade, sexid2): 
    if age and sex and race7 and bmi and grade and sexid2 is not None: 
        year = 2019
        age = age_dict.get(age)
        sex = sex_dict.get(sex)
        race7 = race7_dict.get(race7)
        bmi = bmi_dict.get(bmi)
        grade = grade_dict.get(grade)
        sexid2 = sexid2_dict.get(sexid2)
        sample = [[year, age, sex, grade, race7, bmi, sexid2, 1, 1, 1, 2, 2, 1, 1, 3, 8, 8, 1, 3, 2, 2, 3]]
        try: 
            y_pred = model.predict(sample)
            y_pred_proba = model.predict_proba(sample)
            return f'Classification results are: {y_pred}. Probabilities for each classification are: {y_pred_proba[0]}, {y_pred_proba[1]}, and {y_pred_proba[2]}.'
        except: 
            return 'Unable to predict'

app.config.suppress_callback_exceptions = True

if __name__ == '__main__':
    app.run_server(debug=True)