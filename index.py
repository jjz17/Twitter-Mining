from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

### Import Dash Instance and Pages ###
from app import app
from pages import p1
from pages import p2


# Define the navbar structure
def navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Charts", href="/p1")),
                dbc.NavItem(dbc.NavLink("Insights", href="/p2")),
            ],
            brand="Twitter Friends Analytics",
            brand_href="/",
            color="dark",
            dark=True,
        ),
    ])

    return layout

### Page container ###
page_container = html.Div(
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            # children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        ),
        # represents the URL bar, doesn't render anything
        dcc.Location(
            id='url',
            refresh=False,
        ),
        navbar(),
        # content will be rendered in this element
        html.Div(id='page-content')
    ]
)
### Index Page Layout ###
index_layout = html.Div(
    children=[
        html.H1('Welcome to your Personal Twitter Analytics Dashboard!')
        ,
        dcc.Link(
            children='Go to Page 1',
            href='/p1',
        ),
        html.Br(),
        dcc.Link(
            children='Go to Page 2',
            href='/p2',
        ),
    ]
)
### Set app layout to page container ###
app.layout = page_container
### Assemble all layouts ###
app.validation_layout = html.Div(
    children=[
        page_container,
        index_layout,
        p1.layout,
        p2.layout,
    ]
)
### Update Page Container ###


@app.callback(
    Output(
        component_id='page-content',
        component_property='children',
    ),
    [Input(
        component_id='url',
        component_property='pathname',
    )]
)
def display_page(pathname):
    if pathname == '/':
        return index_layout
    elif pathname == '/p1':
        return p1.layout
    elif pathname == '/p2':
        return p2.layout
    else:
        return '404 Error: Page Not Found'
