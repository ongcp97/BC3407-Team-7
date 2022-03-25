import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app, server
from flask_login import LoginManager, current_user
from methods.User import User
import sqlite3

tabs_styles = {
    'height': '44px',
    'margin': '1rem'
}
tab_style = {
    'borderBottom': '1px solid #0D6EFD',
    'padding': '6px',
}

tab_selected_style = {
    'borderTop': '1px solid #0D6EFD',
    'borderBottom': '1px solid #0D6EFD',
    'backgroundColor': '#0D6EFD',
    'color': 'white',
    'padding': '6px'
}

layout = html.Div([
    html.H5("Dashboard"),
    dcc.Tabs(id="tabs-styled-with-inline", value='dashboard-tab-1', children=[
        dcc.Tab(label='Show Up Rates', value='dashboard-tab-1', style=tab_style, selected_style=tab_selected_style,
                children=html.Div([html.H5('Filter by:'),
                                   dbc.Row([
                                       dbc.Col([
                                           dbc.Row([html.Div(
                                               [dbc.Label('Appointment Date',
                                                          style={'float': 'left', 'margin-right': '1rem'}),

                                                ])
                                           ]),
                                           dbc.Row([dbc.Spinner(dcc.DatePickerRange(id='dashboard-tab-1-appt-date',
                                                                                    clearable=True,
                                                                                    style={'zIndex': '1'}),
                                                                fullscreen=False,
                                                                color='#0D6EFD')])
                                       ]),
                                   ], style={"margin": '1rem'}),
                                   ])
                ),
        dcc.Tab(label='No. of Appointments', value='dashboard-tab-2', style=tab_style, selected_style=tab_selected_style,
                children=html.Div([html.H5('Filter by:'),
                                   dbc.Row([
                                       dbc.Col([
                                           dbc.Row([html.Div(
                                               [dbc.Label('Appointment Date',
                                                          style={'float': 'left', 'margin-right': '1rem'}),

                                                ])
                                           ]),
                                           dbc.Row([dbc.Spinner(dcc.DatePickerRange(id='dashboard-tab-2-appt-date',
                                                                                    clearable=True,
                                                                                    style={'zIndex': '1'}),
                                                                fullscreen=False,
                                                                color='#0D6EFD')])
                                       ]),
                                   ], style={"margin": '1rem'}),
                                   ])

                ),
        dcc.Tab(label='No. of New Patients', value='dashboard-tab-3', style=tab_style, selected_style=tab_selected_style,
                children=html.Div([html.H5('Filter by:'),
                                   dbc.Row([
                                       dbc.Col([
                                           dbc.Row([html.Div(
                                               [dbc.Label('Registered Date',
                                                          style={'float': 'left', 'margin-right': '1rem'}),

                                                ])
                                           ]),
                                           dbc.Row([dbc.Spinner(dcc.DatePickerRange(id='dashboard-tab-3-registered-date',
                                                                                    clearable=True,
                                                                                    style={'zIndex': '1'}),
                                                                fullscreen=False,
                                                                color='#0D6EFD')])
                                       ]),
                                   ], style={"margin": '1rem'}),
                                   ])
                ),
        dcc.Tab(label='Historical Hospital Capacity', value='dashboard-tab-4', style=tab_style,
                selected_style=tab_selected_style,
                children=html.Div([html.H5('Filter by:'),
                                   dbc.Row([
                                       dbc.Col([
                                           dbc.Row([html.Div(
                                               [dbc.Label('Appointment Date',
                                                          style={'float': 'left', 'margin-right': '1rem'}),

                                                ])
                                           ]),
                                           dbc.Row([dbc.Spinner(dcc.DatePickerRange(id='dashboard-tab-4-appt-date',
                                                                                    clearable=True,
                                                                                    style={'zIndex': '1'}),
                                                                fullscreen=False,
                                                                color='#0D6EFD')])
                                       ]),
                                   ], style={"margin": '1rem'}),
                                   ])
                ),
        dcc.Tab(label='Patient Characteristics', value='dashboard-tab-5', style=tab_style,
                selected_style=tab_selected_style,
                children=html.Div([html.H5('Filter by:'),
                                   dbc.Row([
                                       dbc.Col([
                                           dbc.Row([html.Div(
                                               [dbc.Label('Registered Date',
                                                          style={'float': 'left', 'margin-right': '1rem'}),

                                                ])
                                           ]),
                                           dbc.Row([dbc.Spinner(dcc.DatePickerRange(id='dashboard-tab-5-registered-date',
                                                                                    clearable=True,
                                                                                    style={'zIndex': '1'}),
                                                                fullscreen=False,
                                                                color='#0D6EFD')])
                                       ]),
                                   ], style={"margin": '1rem'}),
                                   ])
                ),
    ], style=tabs_styles),
    html.Div(id='tabs-content-output', style={"margin": "1rem"})
])


@app.callback(Output('tabs-content-output', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab): #TODO + Interact with 
    if tab == 'dashboard-tab-1':
        content = html.Div([html.Div('Combo Graph of Show up rates over time'),
                            dcc.Graph(),
                            ])
    elif tab == 'dashboard-tab-2':
        content = html.Div([dcc.Graph(),
                            ])
    elif tab == 'dashboard-tab-3':
        content = html.Div([dcc.Graph(),
                            ])
    elif tab == 'dashboard-tab-4':
        content = html.Div([dcc.Graph(),
                            ])
    elif tab == 'dashboard-tab-5':
        content = html.Div([dcc.Graph(),
                            ])
    return content


# ---------------------------------------------------------------------------------------------------------------------
# Flask-login
# ---------------------------------------------------------------------------------------------------------------------
# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# callback to reload the user object
@login_manager.user_loader
def load_user(username):
    try:
        conn = sqlite3.connect('assets/hospital_database.db')
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM users  WHERE (user_id = '{username}');")
        lu = cursor.fetchone()
        if lu is None:
            return None
        else:
            return User(lu[0], lu[1], lu[2])
    except Exception as e:
        print(e)
        return None