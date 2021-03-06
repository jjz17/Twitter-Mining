from operator import inv
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from torch import positive

# Import Dash Instance
from app import app


def time_to_sent(data: pd.DataFrame) -> pd.DataFrame:
    '''
    Aggregate sentiment counts per user with pivot tables
    data has columns: User, Text, Sentiment, Time
    '''
    data = data.drop(['Text'], axis=1)
    pt = pd.pivot_table(data, values='Time', index='User',
                        columns='Sentiment', aggfunc='count').fillna(0)
    return pt.reset_index()


time_data = pd.read_csv('time_tweet.csv')
time_data['Time'] = pd.to_datetime(time_data['Time'])

summary = time_data.groupby(['Time', ]).count()

color_discrete_map = {
    'Negative': 'rgb(181,14,5)', 'Neutral': 'rgb(230,195,21)', 'Positive': 'rgb(21, 150, 56)', 'Count': 'rgb(21, 150, 56)'}

sentiment_data = pd.read_csv('sentiment.csv').sort_values('User')
agg = sentiment_data['Negative'] + \
    sentiment_data['Neutral'] + sentiment_data['Positive']
sentiment_data['Neg%'] = sentiment_data['Negative'] / agg
sentiment_data['Neu%'] = sentiment_data['Neutral'] / agg
sentiment_data['Pos%'] = sentiment_data['Positive'] / agg
sentiment_data['Total'] = sentiment_data[[
    'Positive', 'Neutral', 'Negative']].sum(axis=1)
sentiment_data.sort_values('Pos%', ascending=False, inplace=True)
# Get DataFrame indices of rows with max in each column
pos = sentiment_data.loc[sentiment_data['Pos%'].idxmax()]
neu = sentiment_data.loc[sentiment_data['Neu%'].idxmax()]
neg = sentiment_data.loc[sentiment_data['Neg%'].idxmax()]
max_total = sentiment_data.loc[sentiment_data['Total'].idxmax()]
min_total = sentiment_data.loc[sentiment_data['Total'].idxmin()]


# Define the page layout
layout = dbc.Container([
    # dbc.Row([
    #     html.Center(html.H1("Page 1")),
    #     html.Br(),
    #     html.Hr(),
    #     dbc.Col([
    #         html.P("This is column 1."),
    #         dbc.Button("Test Button", color="primary")
    #     ]),
    #     dbc.Col([
    #         html.P("This is column 2."),
    #         html.P(
    #             "You can add many cool components using the bootstrap dash components library."),
    #     ])
    # ]),
    html.P("Select Target Post-Time Range"),
    dcc.DatePickerRange(
        id="date-picker-select",
        start_date=time_data['Time'].min(),
        end_date=time_data['Time'].max(),
        min_date_allowed=time_data['Time'].min(),
        max_date_allowed=time_data['Time'].max(),
        initial_visible_month=time_data['Time'].min(),
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card(children=[dbc.CardHeader('Most Positive Friend:'), html.P(id='pos')], color='success', outline=True)),
        dbc.Col(
            dbc.Card(children=[dbc.CardHeader('Most Neutral Friend:'), html.P(id='neu')], color='warning', outline=True)),
        dbc.Col(
            dbc.Card(children=[dbc.CardHeader('Most Negative Friend:'), html.P(id='neg')], color='danger', outline=True)),
        dbc.Col(
            dbc.Card(children=[dbc.CardHeader('Most Frequent Poster:'), html.P(id='most-freq')], color='primary', outline=True)),
        dbc.Col(
            dbc.Card(children=[dbc.CardHeader('Least Frequent Poster:'), html.P(id='least-freq')], color='info', outline=True)),
    ]),
    # dbc.CardGroup([
    #     dbc.Card(html.P('Card 1', style={'border': '10'})),
    #     dbc.Card(html.P('Card 2'))
    # ])
])


@app.callback(
    Output('pos', 'children'),
    Output('neu', 'children'),
    Output('neg', 'children'),
    Output('most-freq', 'children'),
    Output('least-freq', 'children'),
    Input("date-picker-select", "start_date"),
    Input("date-picker-select", "end_date"),
)
def update_cards(start, end):
    data = time_data.loc[(time_data['Time'] >= start)
                         & (time_data['Time'] <= end)]
    temp_sentiment = time_to_sent(data)
    temp_sentiment['Total'] = temp_sentiment[[
        'Positive', 'Neutral', 'Negative']].sum(axis=1)
    temp_sentiment['Neg%'] = temp_sentiment['Negative'] / \
        temp_sentiment['Total']
    temp_sentiment['Neu%'] = temp_sentiment['Neutral'] / \
        temp_sentiment['Total']
    temp_sentiment['Pos%'] = temp_sentiment['Positive'] / \
        temp_sentiment['Total']
    # print(temp_sentiment)
    pos = temp_sentiment.loc[temp_sentiment['Pos%'].idxmax()]
    neu = temp_sentiment.loc[temp_sentiment['Neu%'].idxmax()]
    neg = temp_sentiment.loc[temp_sentiment['Neg%'].idxmax()]
    max_total = temp_sentiment.loc[temp_sentiment['Total'].idxmax()]
    min_total = temp_sentiment.loc[temp_sentiment['Total'].idxmin()]
    # print(pos)
    # print(pos['User'])
    return f'Most positive friend: {pos["User"]} with {pos["Pos%"]*100}% positivity', f'Most neutral friend: {neu["User"]} with {neu["Neu%"]*100}% neutrality', f'Most negative friend: {neg["User"]} with {neg["Neg%"]*100}% negativity', f'Most frequent poster: {max_total["User"]} with {max_total["Total"]} posts', f'Least frequent poster: {min_total["User"]} with {min_total["Total"]} posts'
    # return html.P(f'Success {pos}')
