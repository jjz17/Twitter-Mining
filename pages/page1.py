from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

sentiment_data = pd.read_csv('sentiment.csv').sort_values('User')
agg = sentiment_data['Negative'] + sentiment_data['Neutral'] + sentiment_data['Positive']
sentiment_data['Neg%'] = sentiment_data['Negative'] / agg
sentiment_data['Neu%'] = sentiment_data['Neutral'] / agg
sentiment_data['Pos%'] = sentiment_data['Positive'] / agg
sentiment_data.sort_values('Pos%', ascending=False, inplace=True)
pos = sentiment_data.loc[sentiment_data['Pos%'].idxmax()]
neu = sentiment_data.loc[sentiment_data['Neu%'].idxmax()]
neg = sentiment_data.loc[sentiment_data['Neg%'].idxmax()]

# Define the page layout
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Page 1")),
        html.Br(),
        html.Hr(),
        dbc.Col([
            html.P("This is column 1."),
            dbc.Button("Test Button", color="primary")
        ]),
        dbc.Col([
            html.P("This is column 2."),
            html.P(
                "You can add many cool components using the bootstrap dash components library."),
        ])
    ]),
    dbc.Row([
        dbc.Row([
                dbc.Col(dbc.Card(html.P(f'Most positive friend: {pos.loc["User"]}'))),
                dbc.Col(dbc.Card(html.P(f'Most neutral friend: {neu.loc["User"]}'))),
                dbc.Col(dbc.Card(html.P(f'Most negative friend: {neg.loc["User"]}'))),
                ]),
        dbc.CardGroup([
            dbc.Card(html.P('Card 1', style={'border': '10'})),
            dbc.Card(html.P('Card 2'))
        ])
    ])
])
