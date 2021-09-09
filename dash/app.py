import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import joblib
import dash_pivottable

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
grades89_dict = {'Mostly A\'s': 1, 'Mostly B\'s': 2, 'Mostly C\'s': 3, 'Mostly D\'s': 4, 'Mostly F\'s': 5, 
             'None of these': 6, 'Not sure': 7}
grades89 = ['Mostly A\'s', 'Mostly B\'s', 'Mostly C\'s', 'Mostly D\'s', 'Mostly F\'s', 
             'None of these', 'Not sure']
sleep88_dict = {'4 hours or less': 1, '5 hours': 2, '6 hours': 3, '7 hours': 4, '8 hours': 5, 
             '9 hours': 6, '10 or more hours': 7}
sleep88 = ['4 hours or less', '5 hours', '6 hours', '7 hours', '8 hours', 
             '9 hours', '10 or more hours']
asthma87_dict = {'Yes': 1, 'No': 2, 'Not sure': 3}
asthma87 = ['Yes', 'No', 'Not sure']
concussion83_dict = {'0': 1, '1': 2, '2': 3, '3': 4, '4 or more': 5}
concussion83 = ['0', '1', '2', '3', '4 or more']
teams82_dict = {'0 teams': 1, '1 team': 2, '2 teams': 3, '3 or more teams': 4}
teams82 = ['0 teams', '1 team', '2 teams', '3 or more teams']
videogames80_dict = {'No video games': 1, 'Less than 1 hour': 2, '1 hour': 3, '2 hours': 4, 
                  '3 hours': 5, '4 hours': 6, '5 or more hours': 7}
videogames80 = ['No video games', 'Less than 1 hour', '1 hour', '2 hours', 
                  '3 hours', '4 hours', '5 or more hours']
weight67_dict = {'Very underweight': 1, 'Slightly underweight': 2, 'About the right weight': 3, 
             'Slightly overweight': 4, 'Very overweight': 5}
weight67 = ['Very underweight', 'Slightly underweight', 'About the right weight', 
             'Slightly overweight', 'Very overweight']
breakfast77_dict = {'0 days': 1, '1 day': 2, '2 days': 3, '3 days': 4, '4 days': 5, '5 days': 6, 
                 '6 days': 7, '7 days': 8}
breakfast77 = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', 
                 '6 days', '7 days']
tv79_dict = {'No TV': 1, 'Less than 1 hour': 2, '1 hour': 3, '2 hours': 4, '3 hours': 5, 
          '4 hours': 6, '5 or more hours': 7}
tv79 = ['No TV', 'Less than 1 hour', '1 hour', '2 hours', '3 hours', 
          '4 hours', '5 or more hours']
model = joblib.load('rf_hyp.joblib')

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
    ), 
    # dash_pivottable.PivotTable(
    #   id='pivot,'
    #   data=[df.columns.tolist()] + df.values.tolist(), 
    #   cols=["sex"],
    #   rows=["race7"],
    #   vals=["sitename"],
    # )

        ]),
        dcc.Tab(label='Make Predictions', children=[
            dcc.Markdown('''
            Change the dropdown menus to predict youth risk behavior based on age, gender
            assigned at birth, race/ethnicity, age, grade, and other responses from the survey.'''),
            html.Div(className = 'row', id='prediction-content', style={'fontWeight': 'bold'}),
            html.Div([ 
                dcc.Markdown('How old is this individual?'),
                dcc.Dropdown(
                    id='age', 
                    options=[{'label': age, 'value': age, 'title': 'Age'} for age in age], 
                    value=age[0], 
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('Gender assigned at Birth?'),
                dcc.Dropdown(
                    id='sex', 
                    options=[{'label': sex, 'value': sex, 'title': 'Gender Assigned at Birth'} for sex in sex], 
                    value=sex[0],
                    style=dict(width='100%')
                ),
            ]),
            
            html.Div([ 
                dcc.Markdown('Grade in School?'),
                dcc.Dropdown(
                    id='grade', 
                    options=[{'label': grade, 'value': grade, 'title': 'Grade'} for grade in grade], 
                    value=grade[0],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('Race / Ethnicity?'),
                dcc.Dropdown(
                    id='race7', 
                    options=[{'label': race7, 'value': race7, 'title': 'Race/Ethnicity'} for race7 in race7], 
                    value=race7[0],
                    style=dict(width='100%')
                ),
            ]),

            html.Div(className = 'row', id='prediction-content-2', style={'fontWeight': 'bold'}),

            html.Div([ 
                dcc.Markdown('What is this person\'s BMI?'),
                dcc.Dropdown(
                    id='bmi', 
                    options=[{'label': bmi, 'value': bmi, 'title':'BMI'} for bmi in bmi], 
                    value=bmi[0],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('Sexual Identity?'),
                dcc.Dropdown(
                    id='sexid2', 
                    options=[{'label': sexid2, 'value': sexid2, 'title': 'Sexual Identity'} for sexid2 in sexid2], 
                    value=sexid2[0],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('How would this person describe their weight?'),
                dcc.Dropdown(
                    id='weight67', 
                    options=[{'label': weight67, 'value': weight67, 'title': 'Weight67'} for weight67 in weight67], 
                    value=weight67[2],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('How many days did this individual eat breakfast last week?'),
                dcc.Dropdown(
                    id='breakfast77', 
                    options=[{'label': breakfast77, 'value': breakfast77, 'title': 'Days ate breakfast last week?'} for breakfast77 in breakfast77], 
                    value=breakfast77[3],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('Hours of TV on a school day?'),
                dcc.Dropdown(
                    id='tv79', 
                    options=[{'label': tv79, 'value': tv79, 'title': 'Hours of TV on a school day?'} for tv79 in tv79], 
                    value=tv79[3],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('Hours of Video Games on a school day?'),
                dcc.Dropdown(
                    id='videogames80', 
                    options=[{'label': videogames80, 'value': videogames80, 'title': 'Hours of video games on a school day?'} for videogames80 in videogames80], 
                    value=videogames80[3],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('Number of sports teams last year?'),
                dcc.Dropdown(
                    id='teams82', 
                    options=[{'label': teams82, 'value': teams82, 'title': 'Number of sports teams last year?'} for teams82 in teams82], 
                    value=teams82[3],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('Number of concussions last year?'),
                dcc.Dropdown(
                    id='concussion83', 
                    options=[{'label': concussion83, 'value': concussion83, 'title': 'Number of concussions last year?'} for concussion83 in concussion83], 
                    value=concussion83[3],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('Has this individual ever been told they have asthma?'),
                dcc.Dropdown(
                    id='asthma87', 
                    options=[{'label': asthma87, 'value': asthma87, 'title': 'asthma?'} for asthma87 in asthma87], 
                    value=asthma87[1],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('Hours of Sleep per Night?'),
                dcc.Dropdown(
                    id='sleep88', 
                    options=[{'label': sleep88, 'value': sleep88, 'title': 'Hours of sleep per night?'} for sleep88 in sleep88], 
                    value=sleep88[3],
                    style=dict(width='100%')
                ),
            ]),

            html.Div([ 
                dcc.Markdown('How are this individual\'s current grades?'),
                dcc.Dropdown(
                    id='grades89', 
                    options=[{'label': grades89, 'value': grades89, 'title': 'grades?'} for grades89 in grades89], 
                    value=grades89[0],
                    style=dict(width='100%')
                ),
            ]),

                html.Div(id='predict')
            ], style={'width': '100%', 'display': 'flex', 'display': 'inline-block'},), 

        dcc.Tab(label='Visualize the Connections', children=[
            dcc.Markdown('''The graph network shown below is based on a 
            subsample of 10,000 surveys from the original dataset, maintaining the proportions of target 
            classifications. Each node is a negative risk behavior and the directional edges 
            between the nodes represent the proportion of survey respondents who answered 
            affirmatively to any of those questions. For example, 31.5 percent of respondents who
            reported feeling sad or hopeless for more than 2 weeks in a row also reported getting
            less than 8 hours of sleep on an average school night. This graph may provide some 
            further direction to dashboard users about potentially relevant discussions with youth. Numbers 
            listed are percentages. 
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
  {'data': {'weight': '0.5',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Drink and Drive 30d'}},
   {'data': {'weight': '1.0',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Carry a Weapon 30d'}},
   {'data': {'weight': '1.0',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Felt Unsafe at School'}},
   {'data': {'weight': '3.0',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Felt Sad or Hopeless, 2 wks'}},
   {'data': {'weight': '1.5',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Ever Tried Cigarettes'}},
   {'data': {'weight': '2.1',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '3.5',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '3.3',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '0.2',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '5.8',
     'source': 'Never / Rarely Wear a Seatbelt',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '0.6',
     'source': 'Drink and Drive 30d',
     'target': 'Carry a Weapon 30d'}},
   {'data': {'weight': '0.5',
     'source': 'Drink and Drive 30d',
     'target': 'Felt Unsafe at School'}},
   {'data': {'weight': '1.0',
     'source': 'Drink and Drive 30d',
     'target': 'Felt Sad or Hopeless, 2 wks'}},
   {'data': {'weight': '1.3',
     'source': 'Drink and Drive 30d',
     'target': 'Ever Tried Cigarettes'}},
   {'data': {'weight': '2.1',
     'source': 'Drink and Drive 30d',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '1.9',
     'source': 'Drink and Drive 30d',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '1.7',
     'source': 'Drink and Drive 30d',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '0.5',
     'source': 'Drink and Drive 30d',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '1.8',
     'source': 'Drink and Drive 30d',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '1.5',
     'source': 'Carry a Weapon 30d',
     'target': 'Felt Unsafe at School'}},
   {'data': {'weight': '4.4',
     'source': 'Carry a Weapon 30d',
     'target': 'Felt Sad or Hopeless, 2 wks'}},
   {'data': {'weight': '3.0',
     'source': 'Carry a Weapon 30d',
     'target': 'Ever Tried Cigarettes'}},
   {'data': {'weight': '4.2',
     'source': 'Carry a Weapon 30d',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '5.4',
     'source': 'Carry a Weapon 30d',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '5.0',
     'source': 'Carry a Weapon 30d',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '2.2',
     'source': 'Carry a Weapon 30d',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '7.4',
     'source': 'Carry a Weapon 30d',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '6.0',
     'source': 'Felt Unsafe at School',
     'target': 'Felt Sad or Hopeless, 2 wks'}},
   {'data': {'weight': '2.3',
     'source': 'Felt Unsafe at School',
     'target': 'Ever Tried Cigarettes'}},
   {'data': {'weight': '3.4',
     'source': 'Felt Unsafe at School',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '4.8',
     'source': 'Felt Unsafe at School',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '4.5',
     'source': 'Felt Unsafe at School',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '2.5',
     'source': 'Felt Unsafe at School',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '8.9',
     'source': 'Felt Unsafe at School',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '8.3',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Ever Tried Cigarettes'}},
   {'data': {'weight': '11.8',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '17.9',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '15.6',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '8.6',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '31.5',
     'source': 'Felt Sad or Hopeless, 2 wks',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '8.3',
     'source': 'Ever Tried Cigarettes',
     'target': 'Drank Alcohol, 30d'}},
   {'data': {'weight': '11.6',
     'source': 'Ever Tried Cigarettes',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '9.3',
     'source': 'Ever Tried Cigarettes',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '3.7',
     'source': 'Ever Tried Cigarettes',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '12.7',
     'source': 'Ever Tried Cigarettes',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '17.3',
     'source': 'Drank Alcohol, 30d',
     'target': 'Ever used Marijuana'}},
   {'data': {'weight': '13.7',
     'source': 'Drank Alcohol, 30d',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '5.1',
     'source': 'Drank Alcohol, 30d',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '19.9',
     'source': 'Drank Alcohol, 30d',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '22.0',
     'source': 'Ever used Marijuana',
     'target': 'Ever Had Sex'}},
   {'data': {'weight': '8.4',
     'source': 'Ever used Marijuana',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '30.0',
     'source': 'Ever used Marijuana',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '7.8',
     'source': 'Ever Had Sex',
     'target': 'Watch >3h TV on school days'}},
   {'data': {'weight': '27.5',
     'source': 'Ever Had Sex',
     'target': 'Get <8h Sleep on Avg School Night'}},
   {'data': {'weight': '16.6',
     'source': 'Watch >3h TV on school days',
     'target': 'Get <8h Sleep on Avg School Night'}}
], 
stylesheet=[
            {
            'selector': 'node',
            'style': {
                'label': 'data(label)', 
                'label-scale': 3,
                'background-color': '#0D664CC1'
            }
        },
            {
                'selector': '.interest', 
                'style': {
                    'background-color': '#664CC1', 
                    'shape': 'circle'
                }
            }, 
            {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier', 
                'source-arrow-color': '#8858D4',
                'target-arrow-shape': 'triangle', 
                'line-color': '#0D072B8B', 
                'arrow-scale': 1

            }},  
            {
            'selector': '[weight >= 10]',
            'style': {
                'line-color': '#E6072B8B', 
                'label': 'data(weight)',
                'arrow-scale': 1,
                'width': 5, 
                'target-arrow-shape': 'triangle',
                'target-arrow-color': '#E6072B8B'
            }},
            {
            'selector': '[weight < 10]',
            'style': {
                'line-color': '#0D072B8B', 
                'arrow-scale': .5,
                'width': .5, 
                'target-arrow-shape': 'triangle'
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
    Input('grade', 'value'),
    Input('race7', 'value'), 
    Input('bmi', 'value'),
    Input('sexid2', 'value'), 
    Input('weight67', 'value'), 
    Input('breakfast77', 'value'), 
    Input('tv79', 'value'), 
    Input('videogames80', 'value'), 
    Input('teams82', 'value'), 
    Input('concussion83', 'value'), 
    Input('asthma87', 'value'),
    Input('sleep88', 'value'),
    Input('grades89', 'value')])
def predict(age, sex, grade, race7, bmi, sexid2, weight67, breakfast77, tv79, videogames80, teams82, concussion83, asthma87, sleep88, grades89): 
    if age and sex and grade and race7 and bmi and sexid2 and weight67 and breakfast77 and tv79 and videogames80 and teams82 and concussion83 and asthma87 and sleep88 and grades89 is not None: 
        age = age_dict.get(age)
        sex = sex_dict.get(sex)
        grade = grade_dict.get(grade)
        race7 = race7_dict.get(race7)
        bmi = bmi_dict.get(bmi)
        sexid2 = sexid2_dict.get(sexid2)
        weight67 = weight67_dict.get(weight67)
        breakfast77 = breakfast77_dict.get(breakfast77)
        tv79 = tv79_dict.get(tv79)
        videogames80 = videogames80_dict.get(videogames80)
        teams82 = teams82_dict.get(teams82)
        concussion83 = concussion83_dict.get(concussion83)
        asthma87 = asthma87_dict.get(asthma87)
        sleep88 = sleep88_dict.get(sleep88)
        grades89 = grades89_dict.get(grades89)
        sample = [[21, 2019, age, sex, grade, race7, bmi, sexid2, weight67, breakfast77, tv79, videogames80, teams82, concussion83, asthma87, sleep88, grades89]]
        try: 
            y_pred = model.predict(sample)
            y_pred_proba = model.predict_proba(sample)
            p1 = round(y_pred_proba[0][0][1] * 100, 2)
            p2 = round(y_pred_proba[1][0][1] * 100, 2)
            p3 = round(y_pred_proba[2][0][1] * 100, 2)
            return f'Classification results are: {y_pred}. The probability that this individual has had sex is {p1} percent, that the individual has been sad / hopeless is {p2} percent, and that the individual has tried smoking cigarettes {p3} percent.'
        except: 
            return 'Unable to predict'

app.config.suppress_callback_exceptions = True

if __name__ == '__main__':
    app.run_server(debug=True)