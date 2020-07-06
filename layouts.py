import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# layout1 = html.Div([
#     html.H3('App 1'),
#     dcc.Dropdown(
#         id='app-1-dropdown',
#         options=[
#             {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
#                 'NYC', 'MTL', 'LA'
#             ]
#         ]
#     ),
#     html.Div(id='app-1-display-value'),
#     dcc.Link('Go to App 2', href='/apps/app2')
# ])

# layout2 = html.Div([
#     html.H3('App 2'),
#     dcc.Dropdown(
#         id='app-2-dropdown',
#         options=[
#             {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
#                 'NYC', 'MTL', 'LA'
#             ]
#         ]
#     ),
#     html.Div(id='app-2-display-value'),
#     dcc.Link('Go to App 1', href='/apps/app1')
# ])

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

layout_dev = dbc.Container(
    dbc.Alert("Hello Bootstrap!", color="alert alert-dismissible alert-success"),
    className="p-5",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Mr Anderson", className="ml-2 md-6")),
                ],
                align="center",
                no_gutters=True,
            ),
            # href="https://plot.ly",
        ),
        # dbc.NavbarToggler(id="navbar-toggler"),
        # dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="info",
    dark=True,
)

search = dbc.FormGroup(
    [
        dbc.Label("Sentiment Search"),
        dbc.Input(placeholder="#iknowkungfu", type="text"),
        dbc.FormText("Search for a hashtag in the box above..."),
    ]
)


layout_main = html.Div([
    navbar,
    html.Hr(),
    search
])

