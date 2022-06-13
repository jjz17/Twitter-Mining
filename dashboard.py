from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

data = pd.read_csv('sentiment.csv')
# data = data.query("User == 'NovusOrdoWatch'")

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children='Twitter Friends Analytics',),
        html.P(
            children="Gain insights on the sentiment of your Twitter friends' recent posts.",
        ),
        dcc.Dropdown(
            id='dropdown',
            options=data['User'],
            value=data['User'],
            multi=True
        ),
        dcc.Graph(id='bar')
    ]
)

@app.callback(
    Output('bar', 'figure'), 
    Input('dropdown', 'value'))
def update_bar_chart(users):
    mask = data['User'].isin(users)
    fig = px.bar(data[mask], x='User', y=['Negative', 'Neutral', 'Positive'], labels={'value': 'Count', 'variable': 'Sentiment'})
    return fig

if __name__ == '__main__':
    app.run(debug=True)
