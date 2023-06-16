import time
from dash import Dash, html, dcc, Input, Output, State, dash_table, Patch
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import numpy as np
import math
import json
import dash_bootstrap_components as dbc
import base64
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image

external_stylesheets = [ 
    dbc.icons.FONT_AWESOME
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

darkTheme = False
cyanColor = "rgb(37, 150, 190)"

def round_to_half(number):
    if number < 0:
        return - ( math.ceil(abs(number)*2)/2 )
    return math.ceil(number*2)/2

image = Image.open('assets/drill.png')
rotatePhoneImage = Image.open('assets/rotate-phone-white.png')

theme = {
    'light':{
        'plot_bg_color':'white',
        'dashedLineColor':cyanColor,
        'ticksColor':"black"
    }, 
    'dark':{
        'plot_bg_color':'#061d2c',
        'dashedLineColor':"white",
        'ticksColor':"white"
    }
}

bottom_info = dbc.Col([
                html.Div([
                    html.Div([
                        html.P("GPS POSITION")
                    ], id="gps-div-popover", className="gps-div popover"),
                    html.Div([
                        html.Div([
                            html.P("LAT: ", style={'width':'20px'}),
                            html.P("52.220156 / N 52° 13' 12.561", id="latitude-popover", className="latitude popover"),
                        ], id="long-lat-div-popover-2"),
                        html.Div([
                            html.P("LON: ", style={'width':'20px'}),
                            html.P("20.978256 / E 20° 58' 41.721", id="longtitude-popover", className="longtitude popover"), 
                        ], id="long-lat-div-popover-1"),
                    ], id="long-lat-div-popover", className="long-lat-div popover"),
                ], id="gps-div-outer-popover", className="gps-div-outer popover"),
                html.Div([
                    html.P("LOCAL DATE TIME"),
                    html.P(id="local-time-popover", className="local-time popover"),
                ], id="local-time-div"),
                html.Div([
                    html.P("UTC DATE TIME"),
                    html.P(id="utc-time-popover", className="utc-time popover"),
                ], id="utc-time-div"),
            ], id="bottom-info-popover", className="bottom-col-2 popover"),

def getCurrentDataForGraph():
    data = []
    local_datetime = datetime.now()-timedelta(hours=2)
    while local_datetime <= datetime.now()+timedelta(hours=24):
        data.append([local_datetime, math.sin(local_datetime.timestamp()/9000)+0.1])
        local_datetime += timedelta(hours=1)

    df = pd.DataFrame(data, columns=['X', 'Y'])

    return df

def graphCreation(current_theme):
    df = getCurrentDataForGraph()
    current_time_local_datetime = datetime.now()
    current_time_utc_datetime = datetime.utcnow()
    hours_diff = math.ceil((current_time_local_datetime - current_time_utc_datetime).total_seconds() / 3600)

    tickvals_x = [item-timedelta(minutes=current_time_local_datetime.minute) for item in df['X'] if item.hour % 3 == 0]
    ticktext_x = [f'{local.hour}<br></br><span style="color:{cyanColor}">{ (local-timedelta(hours=hours_diff)).hour }</span>' for local in tickvals_x]

    min_y = round_to_half(df['Y'].min())
    max_y = round_to_half(df['Y'].max())

    actual_draught = 26
    selected_draught = 25
    
    tickvals_y = [i for i in np.arange(min_y-0.5, max_y+0.7, 0.5)]
    ticktext_y = [f'{i} m  ' for i in tickvals_y]

    x_image = df['X'][2]
    y_image = df['Y'][2]

    scatter2 = go.Scatter(
            line=dict(
                color=theme[current_theme]['dashedLineColor'], 
                width=1.2,
                dash='dash'
            ),
            mode='lines',
            showlegend=False,
            hoverinfo='skip',
            x=[x_image for i in np.arange(min_y-2, float(df['Y'][2]), 0.1)], 
            y=[i for i in np.arange(min_y-2, float(df['Y'][2]), 0.1)],
            marker=dict(
                color='blue',
                size=1,
            ),
            cliponaxis=False,
        )

    fig = go.Figure(data=[dict( 
        line=dict(
            color="rgb(37, 150, 190)", 
            shape="spline",
            width=1.2
        ),
        mode='markers+lines',
        marker=dict(
            symbol='square', 
            color='white', 
            line=dict(width=1, color='rgb(37, 150, 190)'), 
            size=8
        ),
        showlegend=False,
        hoverinfo='skip',
        x=df['X'],
        y=df['Y'],
        type='scatter'
    ), scatter2])

    fig.update_layout(
        xaxis=dict(
            tickvals=tickvals_x,
            ticktext=ticktext_x,
            ticks="outside",
            tickfont=dict(
                color=theme[current_theme]['ticksColor']
            ),
            range=[
                (current_time_local_datetime-timedelta(hours=2)), 
                (current_time_local_datetime+timedelta(hours=24))
            ],
            tickmode='array',
            title=None, 
            showgrid=False,
            fixedrange=True,
            rangemode='tozero',
        )
    )

    fig.update_layout(
        annotations=[
            go.layout.Annotation(
                x=0.98, y=max_y+0.3, 
                xref='paper', yref='y',
                text=f'ACTUAL DRAUGHT <b>{actual_draught:.2f} m</b>   SELECTED DRAUGHT <b>{selected_draught:.2f} m</b>', showarrow=False,
                font=dict(size=15, color=theme[current_theme]['ticksColor'])
            ),
            go.layout.Annotation(
                x=0.98, y=min_y-0.3,
                xref='paper', yref='y', 
                text=f'Only effective sea level data is shown', showarrow=False,
                font=dict(size=13, color='rgb(37, 150, 190)')
            )
        ]
    )

    fig.update_yaxes(
        range=[min_y-0.5, max_y+0.7],
        tickformat=".1f", 
        title=None, 
        gridcolor="rgba(245,247,251,1.0)",
        gridwidth=0.1,
        tickvals=tickvals_y,
        ticktext=ticktext_y,
        tickfont=dict(
            color=theme[current_theme]['ticksColor']
        ),
        showgrid=True,
        tickmode='array',
        zeroline=False,
        fixedrange=True,
        )

    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor=theme[current_theme]['plot_bg_color'], 
        # height=500, 
        margin_l=62, 
        margin_r=38,  
        margin_t=0,
        margin_b=10,
    )
    print(darkTheme)

# "rgba(245,247,251,1.0)"

    fig.update_layout(
        images=[
            go.layout.Image(
                source=image,
                xref='x',
                yref='y',
                x = x_image,
                y = y_image,
                sizex=30000000,
                sizey=1,
                xanchor='center',
                yanchor='middle',
                layer="above"
            )
        ]
    )

    return fig

navbar_items =  dbc.Row([
    html.Div([
        dbc.Col([
            html.P("ODFJELL DRILLING")
        ], className="col-1"),
        dbc.Col([
            html.P("Drilling / Rig Heave Operational Guidance")
        ], className="col-2 hiding-col", id="hiding-col-par")
    ], id="nav-left"),
    html.Div([
        dbc.Col([
            dbc.Button([
                html.I(className="fa-solid fa-sun fa-2x")
            ], id="light-mode-btn", className="selected-nav"),
            dbc.Button([
                html.I(className="fa-solid fa-moon fa-2x")
            ], id="dark-mode-btn"),
            html.Div(className="vr hiding-col", style={'borderLeft':'1px solid white', 'height':'25px'}),
            html.Button([
                html.I(className="fa-solid fa-gear fa-2x")
            ], className="hiding-col"),
            html.P("Adam Smith", className="hiding-col") # account name
        ], className="col-1"),
        dbc.Col([
            html.Button([
                html.I(className="fa-solid fa-bars fa-2x") # burger navbar tooggle image
            ], )
        ], className="col-2")
    ], id="nav-right")
], id="navbar")

app.layout = html.Div([
    dbc.Navbar([
        dbc.Container([
            navbar_items
        ])
    ], id="navbar-wrapper"),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Button([
                    "MAIN", 
                ], id="main-button", className="selected"),
                html.Button([
                    "AUX", 
                ], id="aux-button")
            ], id="main-aux-container"),
            dbc.Col([
                html.Button([
                    html.I(className="fa-regular fa-map fa-3x", style={'color':'white'}),
                    ],
                    id="info-btn"
                ),
                dbc.Popover(
                    [dbc.PopoverBody(bottom_info, style={'padding':'10px'})],
                    target="info-btn",
                    trigger="hover",
                    hide_arrow=True,
                    placement="left",
                    offset="80,",
                    id="popover"
                ),
                html.Button(
                    "PDF export"
                ,id='pdf-btn')
            ], id="pdf-export-container")
        ], className="buttons-bar")
    ]),
    html.Div([
        dcc.Graph(
            id="graph",
            figure=graphCreation(current_theme='light'),
            config={'displayModeBar': False},
            style={'height':'65vh'}
        ),
        html.Div([
            html.Img(id='img-el', src=rotatePhoneImage),
            html.P("Rotate your device for better experience", id="rotate-p")
        ], id="img-container"),
    ], id="graph-div", className="graph"), 

    html.Div(id="output"),
    html.Div(id="output-2"),
    html.Div(id="output-3"),
    html.Div(id="output-4"),
    html.Div(id="output-5"),
    html.Div(id="output-6"),

    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P("Bit Depth"),
                    html.P("354.21 m", id="bit-depth"),
                ]),
                html.Div([
                    html.P("Corrected Bit Depth"),
                    html.P("354.21 m",id="corrected-bit-depth"),
                ]),
            ], id="bottom-col-1"),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.P("GPS POSITION")
                    ], id="gps-div", className="gps-div"),
                    html.Div([
                        html.Div([
                            html.P("LAT: ", style={'width':'20px'}),
                            html.P("52.220156 / N 52° 13' 12.561", id="latitude", className="latitude"),
                        ]),
                        html.Div([
                            html.P("LON: ", style={'width':'20px'}),
                            html.P("20.978256 / E 20° 58' 41.721", id="longtitude", className="longtitude"), 
                        ]),
                    ], id="long-lat-div", className="long-lat-div"),
                ], id="gps-div-outer", className="gps-div-outer"),
                html.Div([
                    html.P("LOCAL DATE TIME"),
                    html.P(id="local-time", className="local-time"),
                ]),
                html.Div([
                    html.P("UTC DATE TIME"),
                    html.P(id="utc-time", className="utc-time"),
                ]),
            ], id="bottom-col-2", className="bottom-col-2"),
        ], id="bottom-row")
    ], id="bottom-info"),

    html.Div( className="vl", style={'borderLeft':f'2px dashed {cyanColor}',
        'height':'200px', 
        'position':'absolute',
        'left':'164.5px',
        'top':'630px',
        'backgroundImage': 'linear-gradient(1800deg, transparent, transparent 50%, #fff 50%, #fff 100%), linear-gradient(180deg, red, red, red, red, red);' } ),

    html.Script(src='/assets/main.js', defer=True),

    dcc.Store(id='theme_state', data='light'),

    dcc.Interval(
        id="interval-component",
        interval = 1000, 
        n_intervals=0
    )
])

@app.callback(
    Output('utc-time', 'children'),
    Output('local-time', 'children'),
    Output('utc-time-popover', 'children'),
    Output('local-time-popover', 'children'),
    Output('graph', 'figure', allow_duplicate=True),
    Input('interval-component', 'n_intervals'),
    State('theme_state', 'data'),
    prevent_initial_call=True
)
def update_time_bar_and_graph(n, current_theme):
    current_time_local_datetime = datetime.now()
    current_time_utc_datetime = datetime.utcnow()
    current_time_local = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    hours_diff = current_time_utc_datetime.hour - current_time_local_datetime.hour

    fig = graphCreation(current_theme)

    current_time_utc_str = f'{current_time_utc}'
    current_time_local_str = f'{current_time_local}'
    return current_time_utc_str, current_time_local_str, current_time_utc_str, current_time_local_str, fig

app.clientside_callback(
    """
    function(click1){
        let auxBtn = document.getElementById("aux-button");
        let mainBtn = document.getElementById("main-button");
        console.log(click1);

        auxBtn.classList.add('selected');
        mainBtn.classList.remove('selected');

        return null
    }
    """,
    Output('output', 'children'),
    Input('aux-button', 'n_clicks'),
    prevent_initial_call=True
)

app.clientside_callback(
    """
    function(click1){
        let auxBtn = document.getElementById("aux-button");
        let mainBtn = document.getElementById("main-button");

        auxBtn.classList.remove('selected');
        mainBtn.classList.add('selected');

        return null
    }
    """,
    Output('output-2', 'children'),
    Input('main-button', 'n_clicks'), 
    prevent_initial_call=True
)

app.clientside_callback(
    """
    function(click1){
        let lightBtn = document.getElementById("light-mode-btn");
        let darkBtn = document.getElementById("dark-mode-btn");
        let pdfBtn = document.getElementById("pdf-btn");
        let auxBtn = document.getElementById("aux-button");
        let mainBtn = document.getElementById("main-button");
        let localTimeP = document.getElementById("local-time");
        let bodyElement = document.body;

        darkBtn.classList.add('selected-nav');
        lightBtn.classList.remove('selected-nav');
        
        bodyElement.classList.add('dark');
        pdfBtn.classList.add('dark-pdf');
        auxBtn.classList.add('dark-btn');
        mainBtn.classList.add('dark-btn');
        localTimeP.classList.add('dark-btn');

        return null
    }
    """,
    Output('output-3', 'children'),
    Input('dark-mode-btn', 'n_clicks'),
    prevent_initial_call=True
)

app.clientside_callback(
    """
    function(click1){
        let lightBtn = document.getElementById("light-mode-btn");
        let darkBtn = document.getElementById("dark-mode-btn");
        let pdfBtn = document.getElementById("pdf-btn");
        let auxBtn = document.getElementById("aux-button");
        let mainBtn = document.getElementById("main-button");
        let localTimeP = document.getElementById("local-time");
        let bodyElement = document.body;

        darkBtn.classList.remove('selected-nav');
        lightBtn.classList.add('selected-nav');

        bodyElement.classList.remove('dark');
        pdfBtn.classList.remove('dark-pdf');
        auxBtn.classList.remove('dark-btn');
        mainBtn.classList.remove('dark-btn');
        localTimeP.classList.remove('dark-btn');

        return null
    }
    """, 
    Output('output-4', 'children'),
    Input('light-mode-btn', 'n_clicks'),     
    prevent_initial_call=True
)

@app.callback(
    Output('graph', 'figure', allow_duplicate=True,),
    Output('theme_state', 'data', allow_duplicate=True,),
    Input('dark-mode-btn', 'n_clicks'),
    State('theme_state', 'data'),    
    prevent_initial_call=True
)
def changeToDarkTheme(click, current_theme):
    patched_figure = Patch()

    current_theme = 'dark'

    patched_figure["layout"]["plot_bgcolor"] = "#061d2c"
    patched_figure["layout"]["xaxis"]["tickfont"]["color"] = 'white'
    patched_figure["layout"]["yaxis"]["tickfont"]["color"] = 'white'
    patched_figure["layout"]["annotations"][0]["font"]["color"] = 'white'
    patched_figure["data"][1]["line"]["color"] = "white"

    return patched_figure, current_theme

@app.callback(
    Output('graph', 'figure', allow_duplicate=True,),
    Output('theme_state', 'data', allow_duplicate=True,),
    Input('light-mode-btn', 'n_clicks'),
    State('theme_state', 'data'), 
    prevent_initial_call=True
)
def changeToLightTheme(click, current_theme):
    patched_figure = Patch()

    current_theme = 'light'

    patched_figure["layout"]["plot_bgcolor"] = 'white'
    patched_figure["layout"]["xaxis"]["tickfont"]["color"] = 'black'
    patched_figure["layout"]["yaxis"]["tickfont"]["color"] = 'black'
    patched_figure["layout"]["annotations"][0]["font"]["color"] = 'black'
    patched_figure["data"][1]["line"]["color"] = cyanColor

    return patched_figure, current_theme

if __name__ == "__main__":
    app.run_server(debug=True)
