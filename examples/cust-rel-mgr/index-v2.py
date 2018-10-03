# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import flask
import plotly.plotly as py
from plotly import graph_objs as go
import math
from app import app, server, sf_manager
from apps import opportunities, cases, leads
import os

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <script>
          function helpFunction() {
              alert("Contact Sumanta Bose for help!");
          }
          function updateFunction() {
              alert("Current version 1.0.0. Dashboard is updated. No new updates are available now.");
          }
        </script>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        {%metas%}
        <title>HalcyonAgri Digitization Dashboard | Customer Relationship Management</title>
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
              <a class="navbar-brand" href="https://www.halcyonagri.com" target="_blank">HalcyonAgri</a>
            </div>
            <div class="collapse navbar-collapse" id="myNavbar">
              <ul class="nav navbar-nav">
                <li class="active"><a href="http://halcyon-dashboard.herokuapp.com/index.html">Dashboard</a></li>
                <li class="dropdown">
                    <a href="#" data-toggle="dropdown" class="dropdown-toggle">Apps <b class="caret"></b></a>
                    <ul class="dropdown-menu">
                        <li><a href="#">HalcyonAgri Rubber Supply Chain</a></li>
                        <li><a href="#">Rubber Market Stocks Explorer</a></li>
                        <li><a href="#">Customer Relationship Management</a></li>
                        <li><a href="#">Forex Trading and News Platform</a></li>
                        <li><a href="#">Real-time Global Earthquake Data Map</a></li>
                        <li><a href="#">Real-time Plantation Wind Speed Streaming</a></li>
                        <li><a href="#">Smart Factory Label Classification</a></li>
                        <li><a href="#">Vanguard 500 Index Fund Investor Shares</a></li>
                        <li><a href="#">Industry 4.0 IoT/CPS/GPS tracking</a></li>
                        <li><a href="#">Industry 4.0 Process Automation (IEDs)</a></li>
                        <li><a href="#">HeveaConnect Blockchain Explorer</a></li>
                        <li><a href="#">Your App!</a></li>
                    </ul>
                </li>
                <li class="button" onclick="updateFunction()"><a href="#">Update</a></li>
                <li class="button" onclick="helpFunction()"><a href="#">Help</a></li>
              </ul>
              <ul class="nav navbar-nav navbar-right">
                <li class="dropdown">
                    <a href="#" data-toggle="dropdown" class="dropdown-toggle">
                      <span class="glyphicon glyphicon-user"></span>
                      Gerald Tan <b class="caret"></b>
                    </a>
                    <ul class="dropdown-menu">
                        <li><a href="#">Dashboard</a></li>
                        <li class="divider"></li>
                        <li><a href="#">Profile</a></li>
                        <li><a href="#">Favourites</a></li>
                        <li><a href="#">Contacts</a></li>
                        <li class="divider"></li>
                        <li><a href="#">Logout</a></li>
                    </ul>
                </li>
                <li class="dropdown">
                    <a href="#" data-toggle="dropdown" class="dropdown-toggle">
                      <span class="glyphicon glyphicon-bell"></span>
                      Notifications <b class="caret"></b>
                    </a>
                    <ul class="dropdown-menu">
                        <li><a href="#">Alerts</a></li>
                        <li class="divider"></li>
                        <li><a href="#">Inbox</a></li>
                        <li><a href="#">Drafts</a></li>
                        <li><a href="#">Sent Items</a></li>
                        <li class="divider"></li>
                        <li><a href="#">Trash</a></li>
                    </ul>
                </li>
                <li><a href="#"><span class="glyphicon glyphicon-log-out"></span> Logout</a></li>
              </ul>
            </div>
          </div>
        </nav>

        <!--
        <nav class="navbar">
        </nav> -->
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

app.layout = html.Div(
    [
        # header
        html.Div([

            html.Span("Customer Relationship Management Dashboard", className='app-title'),
            
            html.Div(
                html.Img(src='https://www.halcyonagri.com/wp-content/themes/vw-lawyer-attorney/images/halcyon-logo.png',height="100%")
                ,style={"float":"right","height":"100%"}),
            html.P("Demo Dashboard App using Salesforce API for HalcyonAgri (HeveaConnect)")
            ],
            # 
            className="row header"
            ),

        # tabs
        html.Div([

            dcc.Tabs(
                id="tabs",
                style={"height":"20","verticalAlign":"middle"},
                children=[
                    dcc.Tab(label="Opportunities", value="opportunities_tab"),
                    dcc.Tab(label="Leads", value="leads_tab"),
                    dcc.Tab(id="cases_tab",label="Cases", value="cases_tab"),
                ],
                value="leads_tab",
            )

            ],
            className="row tabs_div"
            ),
       
                
        # divs that save dataframe for each tab
        html.Div(
                sf_manager.get_opportunities().to_json(orient="split"),  # opportunities df
                id="opportunities_df",
                style={"display": "none"},
            ),
        html.Div(sf_manager.get_leads().to_json(orient="split"), id="leads_df", style={"display": "none"}), # leads df
        html.Div(sf_manager.get_cases().to_json(orient="split"), id="cases_df", style={"display": "none"}), # cases df



        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),
        
        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)


@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "opportunities_tab":
        return opportunities.layout
    elif tab == "cases_tab":
        return cases.layout
    elif tab == "leads_tab":
        return leads.layout
    else:
        return opportunities.layout

if __name__ == "__main__":
    # app.run_server(debug=True)
    port = int(os.environ.get('PORT', 9010))
    app.run_server(debug=True, port=port)
