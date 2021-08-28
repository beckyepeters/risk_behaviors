import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

df = pd.read_csv('data/sex.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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

collapse = html.Div(
    [
        dbc.Button(
            'About the Youth Risk Behavior Survey', 
            id='about_yrbs', 
            className = 'mb-3', 
            color='#072B8B', 
            n_clicks=0,
        ),
    dbc.Collapse(
        dbc.Card(dbc.CardBody('''
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
id='collapse', 
is_open=False,
    ),
    ]
)

markdown_text = '''

###### Click the arrows by each section to read more...

<details>
<summary>About the Youth Risk Behavior Survey</summary>

#### About the Youth Risk Behavior Survey:

<p>
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
* Inadequate physical activity</p>

</details>

<details><summary>About the Dashboard</summary>

<p>

This dashboard uses data from the YRBS from 2009-2019. Using a machine learning classification 
algorithm (Random Forest), the dashboard provides probabilities that an individual (student, patient, child, etc) 
has engaged in a risk behavior. 

</p>

</details>

<details><summary>Important Considerations</summary>

<p>

1. Insights over Answers: 
    * Certainly a high probability of a person engaging in an activity does not mean that the individual has indeed made that choice.
2. Discussions over Discipline:  
    * The hope is that adult knowledge of the prevalence of these risk behaviors will lead to more appropriate, 
    relevant conversations with young people about their own health, not punish them with information. 
3. Reality over Determinism: 
    * Even if the model were 100 percent accurate, actual choices are impossible to predict for individual people. 
</p>

</details>

'''


def toggle_collapse(n, is_open): 
    if n: 
        return not is_open
    return is_open

app.layout = html.Div(
    children=[
        html.H1(children='Predicting Youth Risk Behavior'),

    html.Div(children='''
Helping parents and professionals have timely and relevant discussions with youth.    
'''),

    dcc.Markdown(children=markdown_text), 

        dcc.Graph(
        figure=fig
    )
])

app.config.suppress_callback_exceptions = True

if __name__ == '__main__':
    # model = joblib.load('tuned_balanced_rf.sav')
    app.run_server(debug=True)