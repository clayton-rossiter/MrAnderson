import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


# global constants
NAVBAR_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# navbar at top of the page
navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=NAVBAR_LOGO, height="30px")),
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

# search bar for hashtags/account name
search = dbc.FormGroup(
    [
        dbc.Label("Sentiment Search"),
        dbc.Input(placeholder="#iknowkungfu", type="text"),
        dbc.FormText("Search for a hashtag in the box above..."),
    ]
)

# sentiment graph
graph_main = html.Div(

)

# data table
table_main = html.Div(

)

layout_main = html.Div([
    navbar,
    html.Hr(),
    dbc.Row(
        dbc.Col(search, width={'size':'auto','offset':1}, sm=10, md=10)
    )
])

