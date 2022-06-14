from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

sentiment_data = pd.read_csv('sentiment.csv').sort_values('User')
# sentiment_data = sentiment_data.query("User == 'NovusOrdoWatch'")
time_data = pd.read_csv('time_tweet.csv')
# time_data = time_data.groupby(['User', 'Time']).count()
# print(time_data)

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children='Twitter Friends Analytics',),
        html.P(
            children="Gain insights on the sentiment of your Twitter friends' recent posts.",
        ),
        dcc.Dropdown(
            id='dropdown',
            options=sentiment_data['User'],
            value=sentiment_data['User'],
            multi=True
        ),
        dcc.Graph(id='bar'),
        dcc.Graph(id='line')
    ]
)


@app.callback(
    Output('bar', 'figure'),
    Input('dropdown', 'value'))
def update_bar_chart(users):
    mask = sentiment_data['User'].isin(users)
    color_discrete_map = {'Negative': 'rgb(255,0,0)', 'Neutral': 'rgb(255,255,0)', 'Positive': 'rgb(0,255,0)'}
    fig = px.bar(sentiment_data[mask], x='User', y=[
                 'Negative', 'Neutral', 'Positive'], 
                 labels={'value': 'Count', 'variable': 'Sentiment'},
                 color_discrete_map=color_discrete_map)
    return fig


@app.callback(
    Output('line', 'figure'),
    Input('dropdown', 'value'))
def update_line_chart(users):
    fig = px.line(time_data, x='Time', y='User')
    return fig


if __name__ == '__main__':
    app.run(debug=True)
