from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

time_data = pd.read_csv('time_tweet.csv')
time_data['Time'] = pd.to_datetime(time_data['Time'])

sentiment_data = pd.read_csv('sentiment.csv').sort_values('User')
agg = sentiment_data['Negative'] + \
    sentiment_data['Neutral'] + sentiment_data['Positive']
sentiment_data['Neg%'] = sentiment_data['Negative'] / agg
sentiment_data['Neu%'] = sentiment_data['Neutral'] / agg
sentiment_data['Pos%'] = sentiment_data['Positive'] / agg
sentiment_data['Total'] = sentiment_data[['Positive', 'Neutral', 'Negative']].sum(axis=1)
sentiment_data.sort_values('Pos%', ascending=False, inplace=True)
# Get DataFrame indices of rows with max in each column
pos = sentiment_data.loc[sentiment_data['Pos%'].idxmax()]
neu = sentiment_data.loc[sentiment_data['Neu%'].idxmax()]
neg = sentiment_data.loc[sentiment_data['Neg%'].idxmax()]
max_total = sentiment_data.loc[sentiment_data['Total'].idxmax()]
min_total = sentiment_data.loc[sentiment_data['Total'].idxmin()]

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
        dbc.Row([
                dbc.Col(
                    dbc.Card(html.P(f'Most positive friend: {pos.loc["User"]} with {pos.loc["Pos%"]*100}% positivity'))),
                dbc.Col(
                    dbc.Card(html.P(f'Most neutral friend: {neu.loc["User"]} with {neu.loc["Neu%"]*100}% neutrality'))),
                dbc.Col(
                    dbc.Card(html.P(f'Most negative friend: {neg.loc["User"]} with {neg.loc["Neg%"]*100}% negativity'))),
                dbc.Col(
                    dbc.Card(html.P(f'Most frequently posting friend: {max_total.loc["User"]} with {max_total.loc["Total"]} posts'))),
                dbc.Col(
                    dbc.Card(html.P(f'Least frequently posting friend: {min_total.loc["User"]} with {min_total.loc["Total"]} posts'))),
                ]),
        dbc.CardGroup([
            dbc.Card(html.P('Card 1', style={'border': '10'})),
            dbc.Card(html.P('Card 2'))
        ])
    ])
])


# @app.callback(
#     Output('summary', 'figure'),
#     Input("date-picker-select", "start_date"),
#     Input("date-picker-select", "end_date"),
# )
# def update_summary(start, end):
#     data = summary.loc[(summary.index >= start) & (summary.index <= end)]
#     fig = px.bar(data, x=data.index, y='User', title='Total Tweets Retrieved by Day',
#                  labels={'Time': 'Day', 'User': 'Count'}, color_discrete_map=color_discrete_map)
#     return fig