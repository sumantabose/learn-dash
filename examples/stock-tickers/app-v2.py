import dash
import dash_core_components as dcc
import dash_html_components as html

import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
import time

app = dash.Dash('stock-tickers')
server = app.server

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-finance-1.28.0.min.js'

colorscale = cl.scales['9']['qual']['Paired']

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv')
df = pd.read_csv('stock-ticker.csv')
mdf = df # modified df

mdf.loc[df["Stock"]=="AAPL", "Stock"] = "HeaveaPro"
mdf.loc[df["Stock"]=="GOOGL", "Stock"] = "Sinochem"
mdf.loc[df["Stock"]=="TSLA", "Stock"] = "HalcyonAgri"
mdf.loc[df["Stock"]=="COKE", "Stock"] = "CorrieMacColl"
mdf.loc[df["Stock"]=="YHOO", "Stock"] = "AlanLGrant"

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        {%metas%}
        <title>HalcyonAgri Digitization Dashboard | Rubber Stocks Explorer</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <nav class="navbar navbar-inverse">
        <div class="container-fluid">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>                        
            </button>
            <a class="navbar-brand" href="#">HalcyonAgri</a>
          </div>
          <div class="collapse navbar-collapse" id="myNavbar">
            <ul class="nav navbar-nav">
              <li class="active"><a href="#">Dashboard</a></li>
              <li><a href="#">Apps</a></li>
              <li><a href="#">Update</a></li>
              <li><a href="#">Help</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
              <li><a href="#"><span class="glyphicon glyphicon-user"></span> Gerald Tan</a></li>
              <li><a href="#"><span class="glyphicon glyphicon-log-in"></span> Logout</a></li>
            </ul>
          </div>
        </div>
        </nav>
        <nav class="navbar">
        </nav>
        {%app_entry%}
        <footer>
            <nav class="container-fluid text-center navbar-inverse">
              <p>
                <span style="color: #ffffff;">
                  <a style="color: #ffffff;" href="https://sumantabose.me" target="_blank">
                  Developed by Sumanta Bose only for demostration purposes to HalcyonAgri.
                  </a>
                </span>
              </p>
            </nav>
            {%config%}
            {%scripts%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    html.Div([
        html.H2('Rubber Stocks Explorer',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.65em',
                       'margin-left': '7px',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '0'
                       }),
        html.Img(src="https://www.halcyonagri.com/wp-content/themes/vw-lawyer-attorney/images/halcyon-logo.png",
                style={
                    'height': '100px',
                    'float': 'right'
                },
        ),
    ]),
    dcc.Dropdown(
        id='stock-ticker-input',
        options=[{'label': s[0], 'value': str(s[1])}
                 for s in zip(df.Stock.unique(), df.Stock.unique())],
        # value=['AAPL', 'GOOGL'],
        value=['HalcyonAgri', 'HeaveaPro'],
        multi=True
    ),
    html.Div(id='graphs')
], className="container")

def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_graph(tickers):
    graphs = []

    if not tickers:
        graphs.append(html.H3(
            "Select a stock ticker.",
            style={'marginTop': 20, 'marginBottom': 20}
        ))
    else:
        for i, ticker in enumerate(tickers):

            dff = mdf[mdf['Stock'] == ticker]

            candlestick = {
                'x': dff['Date'],
                'open': dff['Open'],
                'high': dff['High'],
                'low': dff['Low'],
                'close': dff['Close'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = bbands(dff.Close)
            bollinger_traces = [{
                'x': dff['Date'], 'y': y,
                'type': 'scatter', 'mode': 'lines',
                'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
                'showlegend': True if i == 0 else False,
                'name': '{} - bollinger bands'.format(ticker)
            } for i, y in enumerate(bb_bands)]
            graphs.append(dcc.Graph(
                id=ticker,
                figure={
                    'data': [candlestick] + bollinger_traces,
                    'layout': {
                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                        'legend': {'x': 0}
                    }
                }
            ))

    return graphs


external_css = ["https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"]

for css in external_css:
    app.css.append_css({"external_url": css})


if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


if __name__ == '__main__':
    # app.run_server(debug=True)
    port = int(os.environ.get('PORT', 9040))
    app.run_server(debug=True, port=port)
