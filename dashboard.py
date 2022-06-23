from time import time
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
from pyparsing import col

sentiment_data = pd.read_csv('sentiment.csv').sort_values('User')
# sentiment_data = sentiment_data.query("User == 'NovusOrdoWatch'")
time_data = pd.read_csv('time_tweet.csv')
time_data['Time'] = pd.to_datetime(time_data['Time'])

summary = time_data.groupby(['Time', ]).count()

app = Dash(__name__)


def get_time_line_data(df):
    new_data = pd.DataFrame(columns=['Date', 'Sentiment', 'Count'])
    neg = df[df['Sentiment'] == 'Negative']
    neu = df[df['Sentiment'] == 'Neutral']
    pos = df[df['Sentiment'] == 'Positive']
    for frame, sentiment in zip([neg, neu, pos], ['Negative', 'Neutral', 'Positive']):
        frame = frame.groupby('Time').count()
        for i, date in enumerate(frame.index):
            row = pd.DataFrame([{'Date': date, 'Sentiment': sentiment,
                                'Count': frame.loc[date]['User']}])
            new_data = pd.concat([new_data, row], ignore_index=True)
    return new_data


def description_card():
    '''
    Return a div containing dashboard title and descriptions
    '''
    return html.Div(
        id='description-card',
        children=[
            html.H5('Twitter Friends Analytics'),
            html.H3('Welcome to the Twitter Friends Analytics Dashboard'),
            html.Div(
                id='intro',
                children=('Explore trends in the sentiments of tweets posted by your Twitter friends. '
                          'Use the dropdown menu and date picker to filter for your desired data. Hover over the bars for a focused view of a friend of choice.'),
            ),
        ],
    )


def generate_control_card():
    '''
    Returns a div containing controls for the graphs
    '''
    return html.Div(
        id="control-card",
        children=[
            html.P("Select User(s)"),
            dcc.Dropdown(
                id="users-select",
                options=[{"label": i, "value": i}
                         for i in pd.concat([pd.Series('All'), sentiment_data['User']])],
                value='All',
                multi=True
            ),
            html.P("Sort By"),
            dcc.Dropdown(
                id='sort-select',
                options=['Alphabetical', 'Tweet Count'],
                # value='Alphabetical'
            ),
            html.P("Filter Sentiment"),
            dcc.Dropdown(
                id='sentiment-select',
                options=[{"label": i, "value": i}
                         for i in ['Negative', 'Neutral', 'Positive']],
                value=['Negative', 'Neutral', 'Positive'],
                multi=True
            ),
            html.Br(),
            html.P("Select Post Time"),
            dcc.DatePickerRange(
                id="date-picker-select",
                start_date=time_data['Time'].min(),
                end_date=time_data['Time'].max(),
                min_date_allowed=time_data['Time'].min(),
                max_date_allowed=time_data['Time'].max(),
                initial_visible_month=time_data['Time'].min(),
            ),
            dcc.Checklist(
                id='norm',
                options=['Normalize'],
                value=[]
            )
            # html.Br(),
            # html.Br(),
            # html.P("Select Admit Source"),
            # dcc.Dropdown(
            #     id="admit-select",
            #     options=[{"label": i, "value": i} for i in admit_list],
            #     value=admit_list[:],
            #     multi=True,
            # ),
            # html.Br(),
            # html.Div(
            #     id="reset-btn-outer",
            #     children=html.Button(
            #         id="reset-btn", children="Reset", n_clicks=0),
            # ),
        ],
    )


# app.layout = html.Div(
#     children=[
#         html.H1(children='Twitter Friends Analytics',),
#         html.P(
#             children='Gain insights on the sentiment of your Twitter friends" recent posts.',
#         ),
#         dcc.Dropdown(
#             id='dropdown',
#             options=sentiment_data['User'],
#             value=sentiment_data['User'],
#             multi=True
#         ), dcc.DatePickerRange(
#             id='date-picker-select',
#             start_date=time_data['Time'].min(),
#             end_date=time_data['Time'].max(),
#             min_date_allowed=time_data['Time'].min(),
#             max_date_allowed=time_data['Time'].max(),
#             initial_visible_month=time_data['Time'].min(),
#         ),
#         html.Div([
#             dcc.Graph(id='bar'),
#             dcc.Graph(id='single')], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
#         # dcc.Graph(id='bar'),
#         # dcc.Graph(id='single'),
#         html.Div([dcc.Graph(id='summary', figure=px.bar(summary, x=summary.index, y='User')), dcc.Graph(id='line')], style={
#                  'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
#         # dash_table.DataTable(time_data.to_dict('records'), [{"name": i, "id": i} for i in time_data.columns],
#         #                      fixed_rows={'headers': True},
#         #                      style_table={'height': 400}, id='data')  # defaults to 500)
#         dash_table.DataTable(id='data-table', fixed_rows={'headers': True},
#                              style_table={'height': 400, 'overflowX': 'scroll'})
#     ]
# )


app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            # children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Div([
                    dcc.Graph(id='bar'),
                    dcc.Graph(id='single')], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
                # dcc.Graph(id='bar'),
                # dcc.Graph(id='single'),
                html.Div([dcc.Graph(id='summary', figure=px.bar(summary, x=summary.index, y='User')), dcc.Graph(id='line')], style={
                    'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
                # dash_table.DataTable(time_data.to_dict('records'), [{"name": i, "id": i} for i in time_data.columns],
                #                      fixed_rows={'headers': True},
                #                      style_table={'height': 400}, id='data')  # defaults to 500)
                dash_table.DataTable(id='data-table', fixed_rows={'headers': True},
                                     style_table={'height': 400, 'overflowX': 'scroll'})
            ],
        ),
    ],
)


@app.callback(
    Output('bar', 'figure'),
    Input('users-select', 'value'),
    Input('sort-select', 'value'),
    Input("date-picker-select", "start_date"),
    Input("date-picker-select", "end_date"),)
def update_bar_chart(users, sort, start, end):
    if 'All' in users:
        data = sentiment_data
    else:
        mask = sentiment_data['User'].isin(users)
        data = sentiment_data[mask]

    if sort == 'Alphabetical':
        data = data.sort_values('User')
        print(sort)
    elif sort == 'Tweet Count':
        data['total count'] = data[['Negative',
                                    'Neutral', 'Positive']].sum(axis=1)
        data = data.sort_values('total count')
        data.drop('total count', axis=1, inplace=True)
        print(sort)

    color_discrete_map = {
        'Negative': 'rgb(255,0,0)', 'Neutral': 'rgb(255,255,0)', 'Positive': 'rgb(0,255,0)'}
    fig = px.bar(data, x='User', y=[
                 'Negative', 'Neutral', 'Positive'],
                 labels={'value': 'Count', 'variable': 'Sentiment'},
                 color_discrete_map=color_discrete_map, title='Aggregate Sentiment Count per User')
    fig.update_layout(clickmode='event+select')
    return fig


@app.callback(
    Output('single', 'figure'),
    Output('data-table', 'data'),
    Output('data-table', 'columns'),
    Input('bar', 'hoverData'))
def display_hover_data(hoverData):
    if hoverData:
        user = hoverData['points'][0]['x']
    else:
        user = 'kennedyhall'
    fig = px.bar(sentiment_data[sentiment_data['User'] == user], x='User', y=[
                 'Negative', 'Neutral', 'Positive'], title='Tweets by Selected User')
    data = time_data[time_data['User'] == user]
    table_data = data.to_dict('records')
    columns = [{'name': i, 'id': i} for i in data.columns]
    return fig, table_data, columns


@app.callback(
    Output('summary', 'figure'),
    Input("date-picker-select", "start_date"),
    Input("date-picker-select", "end_date"),
)
def update_summary(start, end):
    data = summary.loc[(summary.index >= start) & (summary.index <= end)]
    fig = px.bar(data, x=data.index, y='User', title='Total Tweets Retrieved by Day',
                 labels={'Time': 'Day', 'User': 'Count'},)
    return fig


@app.callback(
    Output('line', 'figure'),
    Input('users-select', 'value'),
    Input('sentiment-select', 'value'),
    Input('norm', 'value'))
def update_line_chart(users, sentiments, norm):
    if users == 'All' or 'All' in users:
        line_data = time_data
    else:
        line_data = time_data[time_data['User'].isin(users)]
    line_data = get_time_line_data(line_data)
    line_data = line_data[line_data['Sentiment'].isin(sentiments)]
    if norm:
        norm_data = pd.DataFrame(columns=['Date', 'Sentiment', 'Count'])
        for date in line_data['Date'].unique():
            temp = line_data[line_data['Date'] == date]
            sum = temp['Count'].sum()
            for i, row in temp.iterrows():
                norm_row = row
                norm_row.loc['Count'] = row.loc['Count'] / sum
                print(norm_row, type(norm_row))
                norm_row = pd.DataFrame([{'Date': norm_row.loc['Date'], 'Sentiment': norm_row.loc['Sentiment'], 'Count': norm_row.loc['Count']}])
                norm_data = pd.concat([norm_data, norm_row], ignore_index=True)
            # row = pd.DataFrame([{'Date': date, 'Sentiment': sentiment,
            #                     'Count': frame.loc[date]['User']}])
            # new_data = pd.concat([new_data, row], ignore_index=True)
        line_data = norm_data
        print(line_data)
    fig = px.line(line_data, x='Date', y='Count', title='Trends in Sentiment Count', color='Sentiment')
    return fig


if __name__ == '__main__':
    app.run(debug=True)



'''
                   Date Sentiment Count
0   2022-06-10 00:00:00  Negative     6
1   2022-06-14 00:00:00  Negative    24
2   2022-06-15 00:00:00  Negative    28
3   2022-06-16 00:00:00  Negative    21
4   2022-06-17 00:00:00  Negative    38
5   2022-06-20 00:00:00  Negative    18
6   2022-06-21 00:00:00  Negative    27
7   2022-06-22 00:00:00  Negative    78
8   2022-06-23 00:00:00  Negative    23
9   2022-06-10 00:00:00   Neutral    20
10  2022-06-14 00:00:00   Neutral    52
11  2022-06-15 00:00:00   Neutral    52
12  2022-06-16 00:00:00   Neutral    60
13  2022-06-17 00:00:00   Neutral    51
14  2022-06-20 00:00:00   Neutral    66
15  2022-06-21 00:00:00   Neutral    58
16  2022-06-22 00:00:00   Neutral   161
17  2022-06-23 00:00:00   Neutral    60
18  2022-06-10 00:00:00  Positive     4
19  2022-06-14 00:00:00  Positive    24
20  2022-06-15 00:00:00  Positive    20
21  2022-06-16 00:00:00  Positive    19
22  2022-06-17 00:00:00  Positive    11
23  2022-06-20 00:00:00  Positive    16
24  2022-06-21 00:00:00  Positive    15
25  2022-06-22 00:00:00  Positive    61
26  2022-06-23 00:00:00  Positive    17
'''