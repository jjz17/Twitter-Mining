from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Import Dash Instance
from app import app


color_discrete_map = {
    'Negative': 'rgb(181,14,5)', 'Neutral': 'rgb(230,195,21)', 'Positive': 'rgb(21, 150, 56)', 'Count': 'rgb(21, 150, 56)'}


# Layout and Callbacks

def get_data():
    sentiment_data = pd.read_csv('sentiment.csv').sort_values('User')
    # sentiment_data = sentiment_data.query("User == 'NovusOrdoWatch'")
    time_data = pd.read_csv('time_tweet.csv')
    time_data['Time'] = pd.to_datetime(time_data['Time'])
    summary = time_data.groupby(['Time', ]).count()
    return sentiment_data, time_data, summary


# def get_time_line_data(df):
#     new_data = pd.DataFrame(columns=['Date', 'Sentiment', 'Count'])
#     neg = df[df['Sentiment'] == 'Negative']
#     neu = df[df['Sentiment'] == 'Neutral']
#     pos = df[df['Sentiment'] == 'Positive']
#     for frame, sentiment in zip([neg, neu, pos], ['Negative', 'Neutral', 'Positive']):
#         frame = frame.groupby('Time').count()
#         for i, date in enumerate(frame.index):
#             row = pd.DataFrame([{'Date': date, 'Sentiment': sentiment,
#                                 'Count': frame.loc[date]['User']}])
#             new_data = pd.concat([new_data, row], ignore_index=True)
#     return new_data


def description_card():
    '''
    Return a div containing dashboard title and descriptions
    '''
    return html.Div(
        id='description-card',
        children=[
            # html.H5('Twitter Friends Analytics'),
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
    sentiment_data, time_data, summary = get_data()
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
                value='Alphabetical'
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
                options=['Normalize Line Data'],
                value=[]
            )
        ],
    )


def home_content():
    sentiment_data, time_data, summary = get_data()
    return html.Div(children=[
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card(),
                    html.Div(["initial child"], id="output-clientside",
                             style={"display": "none"}),
                    html.Button('Collect Data', id='collect'),
                    html.Div(id='collect_container')
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
            ],)
    ])


'''
Layout
'''
layout = home_content()


@app.callback(
    Output('bar', 'figure'),
    Input('users-select', 'value'),
    Input('sort-select', 'value'),
    Input("date-picker-select", "start_date"),
    Input("date-picker-select", "end_date"),)
def update_bar_chart(users, sort, start, end):
    sentiment_data, time_data, summary = get_data()
    if 'All' in users:
        data = sentiment_data
    else:
        mask = sentiment_data['User'].isin(users)
        data = sentiment_data[mask]

    if sort == 'Alphabetical':
        data = data.sort_values('User')
    elif sort == 'Tweet Count':
        data['total count'] = data[['Negative',
                                    'Neutral', 'Positive']].sum(axis=1)
        data = data.sort_values('total count')
        data.drop('total count', axis=1, inplace=True)

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
    sentiment_data, time_data, summary = get_data()
    if hoverData:
        user = hoverData['points'][0]['x']
    else:
        user = 'kennedyhall'
    fig = px.bar(sentiment_data[sentiment_data['User'] == user], x='User', y=[
                 'Negative', 'Neutral', 'Positive'], title='Tweets by Selected User',
                 labels={'value': 'Count', 'variable': 'Sentiment'}, color_discrete_map=color_discrete_map)
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
    sentiment_data, time_data, summary = get_data()
    data = summary.loc[(summary.index >= start) & (summary.index <= end)]
    fig = px.bar(data, x=data.index, y='User', title='Total Tweets Retrieved by Day',
                 labels={'Time': 'Day', 'User': 'Count'}, color_discrete_map=color_discrete_map)
    return fig


@app.callback(
    Output('line', 'figure'),
    Input('users-select', 'value'),
    Input('sentiment-select', 'value'),
    Input('norm', 'value'))
def update_line_chart(users, sentiments, norm):
    sentiment_data, time_data, summary = get_data()
    # If all users are selected
    if users == 'All' or 'All' in users:
        line_data = time_data
    else:
        line_data = time_data[time_data['User'].isin(users)]
    line_data = pd.pivot_table(
        line_data, values='User', index='Time', columns='Sentiment', aggfunc='count')
    # Select subset of desired sentiment columns
    line_data = line_data[sentiments]
    pd.options.plotting.backend = 'plotly'
    fig = line_data.plot(y=sentiments, title='Trends in Sentiment Count',
                         color_discrete_map=color_discrete_map, labels={'variable': 'Sentiment', 'value': 'Count'})
    if norm:
        line_data['Total'] = line_data[sentiments].sum(axis=1)
        # Scale all sentiments to their percentages
        for sentiment in sentiments:
            line_data[sentiment] = line_data[sentiment] / line_data['Total']
            fig = line_data.plot(y=sentiments, title='Trends in Sentiment Frequency', color_discrete_map=color_discrete_map, labels={
                                 'variable': 'Sentiment', 'value': 'Percentage'})
    return fig


@app.callback(Output('collect_container', 'children'),
              Input('collect', 'n_clicks'))
def collect_data(n_clicks):
    if n_clicks:
        # script_path = 'test1.py'
        script_path = 'data_pipeline.py'
        exec(open(script_path).read())
        # return html.Div(f'Data collected {n_clicks} time(s)')
        return html.Div(f'Data collected successfully!')
