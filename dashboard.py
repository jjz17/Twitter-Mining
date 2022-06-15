import click
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd

sentiment_data = pd.read_csv('sentiment.csv').sort_values('User')
# sentiment_data = sentiment_data.query("User == 'NovusOrdoWatch'")
time_data = pd.read_csv('time_tweet.csv')
neg = time_data[time_data['Sentiment'] == 'Negative']
neu = time_data[time_data['Sentiment'] == 'Neutral']
pos = time_data[time_data['Sentiment'] == 'Positive']
new_data = pd.DataFrame(columns=['Date', 'Sentiment', 'Count'])
for frame, sentiment in zip([neg, neu, pos], ['Negative', 'Neutral', 'Positive']):
    frame = frame.groupby('Time').count()
    for i, date in enumerate(frame.index):
        row = pd.DataFrame([{'Date': date, 'Sentiment': sentiment,
                             'Count': frame.loc[date]['User']}])
        new_data = pd.concat([new_data, row], ignore_index=True)

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
        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data'),
        ]),
        dcc.Graph(id='single'),
        dcc.Graph(id='line'),
        dash_table.DataTable(time_data.to_dict('records'), [{"name": i, "id": i} for i in time_data.columns],
                             fixed_rows={'headers': True},
                             style_table={'height': 400})  # defaults to 500)
    ]
)


@app.callback(
    Output('bar', 'figure'),
    Input('dropdown', 'value'))
def update_bar_chart(users):
    mask = sentiment_data['User'].isin(users)
    color_discrete_map = {
        'Negative': 'rgb(255,0,0)', 'Neutral': 'rgb(255,255,0)', 'Positive': 'rgb(0,255,0)'}
    fig = px.bar(sentiment_data[mask], x='User', y=[
                 'Negative', 'Neutral', 'Positive'],
                 labels={'value': 'Count', 'variable': 'Sentiment'},
                 color_discrete_map=color_discrete_map)
    fig.update_layout(clickmode='event+select')
    return fig


@app.callback(
    Output('single', 'figure'),
    Input('bar', 'hoverData'))
def display_click_data(hoverData):
    if hoverData:
        user = hoverData['points'][0]['x']
    else:
        user = 'kennedyhall'
    fig = px.bar(sentiment_data[sentiment_data['User'] == user], x='User', y=['Negative', 'Neutral', 'Positive'])
    return fig


@app.callback(
    Output('line', 'figure'),
    Input('dropdown', 'value'))
def update_line_chart(users):
    fig = px.line(new_data, x='Date', y='Count', color='Sentiment')
    return fig


if __name__ == '__main__':
    app.run(debug=True)
