import json
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image, ImageFont, ImageDraw

# Function to create the image
def create_image(size_big, size_small):
    # Create an empty image
    image_size = (1100, 1100)
    image = Image.new('L', image_size, color='black')  # Use 'black' instead of 255 for a black background

    # Draw the number "10" on the image
    draw = ImageDraw.Draw(image)
    font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size_big)
    text = "10"
    textwidth, textheight = font_big.getbbox(text)[2:4]
    x = (image_size[0] - textwidth) / 2
    y = (image_size[1] / 3 - textheight) / 3
    draw.text((x, y), text, font=font_big, fill='white')  # Use 'white' instead of 0 for white text

    # Draw "Congratulations" and "Plotly!" on the image
    font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size_small)
    text = "Congratulations"
    textwidth, textheight = font_small.getbbox(text)[2:4]
    x = (image_size[0] - textwidth) / 2
    y = image_size[1] / 2
    draw.text((x, y), text, font=font_small, fill='white')  # Use 'white' instead of 0 for white text

    text = "Plotly!"
    textwidth, textheight = font_small.getbbox(text)[2:4]
    x = (image_size[0] - textwidth) / 2
    y = image_size[1] / 2 + textheight
    draw.text((x, y), text, font=font_small, fill='white')  # Use 'white' instead of 0 for white text

    # Convert the image to a NumPy array
    data = np.array(image)

    return data


# Function to create a scatter plot
# Function to create a scatter plot
def create_scatter(N=100):
    random_x = np.random.randn(N)
    random_y = np.random.randn(N)

    # Random colors for 'confetti'
    colors = ['#%06X' % np.random.randint(0, 0xFFFFFF) for _ in range(N)]

    fig = go.Figure(data=go.Scattergl(
        x = random_x,
        y = random_y,
        mode='markers',
        marker=dict(
            color=colors,
            size=10,
            line=dict(
                color='DarkSlateGrey',
                width=2
            )
        )
    ))

    fig.update_layout(
        autosize=True,
        plot_bgcolor='#010001',
        paper_bgcolor='#010001',
        font_color="white",
        showlegend=False,
        xaxis=dict(range=[-4, 4], title="Confetti 😊"),  # added title
        yaxis=dict(range=[-4, 4]),
        margin=dict(l=0, r=0, b=0, t=0)  # remove margins
    )
    return fig


# Function to create a line 
def create_line():
    # Load data from the JSON file
    with open('./data/data.json', 'r') as f:
        loaded_json = f.read()

        # Decode the JSON twice
        data = json.loads(json.loads(loaded_json))['data']

    df = pd.DataFrame(data)
    
    fig = px.line(df, x="date", y="downloads")
    fig.update_layout(
        autosize=True,
        plot_bgcolor='#010001',
        paper_bgcolor='#010001',
        font_color="white",
        showlegend=False,
    )
    return fig


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(style={'position': 'relative', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'flex-direction': 'row', 'height': '100vh', 'backgroundColor': '#010001'}, children=[
    html.Div(style={'position': 'absolute', 'top': 0, 'left': 0}, children=[html.Img(src='https://media.giphy.com/media/MViYNpI0wx69zX7j7w/giphy.gif')]),
    html.Div(style={'position': 'absolute', 'top': 0, 'right': 0}, children=[html.Img(src='https://media.giphy.com/media/MViYNpI0wx69zX7j7w/giphy.gif')]),
    html.Div(style={'position': 'absolute', 'bottom': 0, 'left': 0}, children=[html.Img(src='https://media.giphy.com/media/MViYNpI0wx69zX7j7w/giphy.gif')]),
    html.Div(style={'position': 'absolute', 'bottom': 0, 'right': 0}, children=[html.Img(src='https://media.giphy.com/media/MViYNpI0wx69zX7j7w/giphy.gif')]),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Graph(
        id='scatter-graph',
        figure=create_scatter()
    ),
    html.Div(style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'flex-direction': 'column'}, children=[
        html.Div(children=[
            dcc.Slider(
                id='size-big',
                min=100,
                max=1000,
                step=10,
                value=600,
                marks={i: '' for i in range(100, 1100, 100)},
            ),
        ], style={'margin': '20px', 'width': '80%'}),

        html.Div(children=[
            dcc.Slider(
                id='size-small',
                min=50,
                max=200,
                step=10,
                value=80,
                marks={i: '' for i in range(50, 600, 50)},
            ),
        ], style={'margin': '20px', 'width': '80%'}),

        html.Div(children=[
            dcc.Graph(
                id='example-graph'
            )
        ], style={'textAlign': 'center'}),
    ]),

    dcc.Graph(
        id='line-graph',
        figure=create_line()
    ),

    html.Div(children=[
    html.P("Best wishes from Danny Bharat and the team at Arkimetrix Analytics", className="scrolling-text"),
], style={'position': 'fixed', 'bottom': '0', 'width': '100%', 'textAlign': 'center'}),
])

@app.callback(
    Output('example-graph', 'figure'),
    [Input('size-big', 'value'), Input('size-small', 'value')]
)
def update_graph(size_big, size_small):
    data = create_image(size_big, size_small)
    
    fig = px.imshow(data, color_continuous_scale='gray')
    fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    fig.update_layout(
        autosize=True,
        plot_bgcolor='#010001',
        paper_bgcolor='#010001',
        font_color="white",
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, b=0, t=0)
    )
    return fig

# And this callback
@app.callback(Output('scatter-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    return create_scatter()

if __name__ == '__main__':
    app.run_server(debug=True)
