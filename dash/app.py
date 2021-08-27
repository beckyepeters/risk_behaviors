import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

df = pd.read_csv('data/sex.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
Helping parents and professionals have timely and relevant discussions with youth.    
'''),
        dcc.Graph(
        figure=fig
    )
])

app.config.suppress_callback_exceptions = True

if __name__ == '__main__':
    # model = joblib.load('tuned_balanced_rf.sav')
    app.run_server(debug=True)