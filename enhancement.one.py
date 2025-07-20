
# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import Dash
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Regular Expression support
import re



# Import AnimalShelter CRUD package
from AnimalShelter import AnimalShelter

###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name

username = "aacuser"
password = "aacuser"

# Connect to database via CRUD Module
db = AnimalShelter(username, password)

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)

#  It's better to do this in the CRUD layer,
#    doing it here makes the dataframe too complex
#    to serialize as JSON. Took way too much debugging
#    to figure that out :)
#
#df.drop(columns=['_id'],inplace=True)


#########################
# Dashboard Layout / View
#########################

# change to not use Jupyter
app = Dash(__name__)

#Add in Grazioso Salvare’s logo
image_filename = 'enhancement.one.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#P lace the HTML image tag in the line below into the app.layout code according to your design
# include a unique identifier such as your name or date

app.layout = html.Div([
#    html.Div(id='hidden-div', style={'display':'none'}),
     html.Div(
        className="row",
        style={"display": "flex"},
        children=[
        html.A([html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
               alt = "Salvare Logo", height = 100, width = 150))], href = "https://www.snhu.edu"),
        html.Center(html.B(html.H1('CS-340 Dashboard - Russ Savela -  Project Two')))
         ]
     ),
    html.Hr(),
        
  #Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.
    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'Reset', 'value': 'ALL'},
            {'label':'Disaster Rescue and Tracking', 'value':'DISASTER'},
            {'label':'Water Rescue', 'value': 'WATER'},
            {'label':'Mountain and Wilderness Rescue', 'value': 'MOUNTAIN'},

        ],
        value='ALL'
    ),
        
    html.Hr(),
      #Set up the features for  interactive data table to make it user-friendly for your client
    dash_table.DataTable(id='datatable-id',
                         columns=[
                             {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
                         ],
                         data=df.to_dict('records'),
                         editable=False,
                         page_action = "native",
                         page_current = 0,
                         page_size = 8,             # limit records displayed
                         sort_action = "native",    # allow sorting
                         filter_action = "native",  # enable filtering
                         row_selectable = "single", # don't confuse the map
                         selected_rows= [0]
                        ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
                 html.Div([
                    dcc.Dropdown(
                        id='chart_dropdown',
                        className='col s12 m6',
                        options=[
                            {'label': 'Breed', 'value': 'breed'},
                            {'label': 'Age', 'value': 'age_upon_outcome'},       
                        ],
                        value='breed',
                        multi=False
                        )
                    ],
                style={"width":"10%"}
                ),           
            html.Div(
                id='graph-id',
                className='col s12 m6',
            ),
            html.Div(
                id='map-id',
                className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################


   
    
@app.callback([Output('datatable-id','data'),
               Output('datatable-id','columns')],
               Input('filter-type', 'value'))
def update_dashboard(filter_type):

    # Regular expressions are used here, because these are 
    # rescue dogs, so we aren't expecting dogs with papers,
    # there are a lot of mixes...

    if filter_type == "ALL":
        
        df = pd.DataFrame.from_records(db.read({}))
                                       
    
    # Disaster or Tracking dog parameters:
    # Doberman Pinscher, German Shepherd, Golden Retriever, Bloodhound, Rottweiler
    # Intact Male 20 weeks to 300 weeks
                                       
    elif filter_type == "DISASTER":
        # Use regular expressions to match
                                                                      
        df = pd.DataFrame.from_records(db.read({
            '$or': [
                {"breed": {'$regex': re.compile(".*doberman.*", re.IGNORECASE) }},
                {"breed": {'$regex': re.compile(".*rott.*", re.IGNORECASE) }},
                {"breed": {'$regex': re.compile(".*bloodh.*", re.IGNORECASE) }},
                {"breed": {'$regex': re.compile(".*golden.*", re.IGNORECASE) }},
                {"breed": {'$regex': re.compile(".*german.*", re.IGNORECASE) }}
            ],
            "age_upon_outcome_in_weeks": {"$gte":20.0, "$lte":300.0},
            "sex_upon_outcome": "Intact Male",
            
        } ))
      
    
    #Labrador Retriever Mix, Chesapeake Bay Retriever,Newfoundland
    #Intact Female 26 weeks to 156  weeks
  
    elif filter_type == "WATER":
                               
        df = pd.DataFrame.from_records(db.read({
            '$or': [
                {"breed": {'$regex': re.compile(".*labrador.*mix.*", re.IGNORECASE) }},
                {"breed": {'$regex': re.compile(".*chesapeake.*", re.IGNORECASE) }},
                {"breed": {'$regex': re.compile(".*newfoundland.*", re.IGNORECASE) }},
            ],
            "age_upon_outcome_in_weeks": {"$gte":26.0, "$lte":156.0},
            "sex_upon_outcome": "Intact Female",} ))
    
    #German Shepherd, Alaskan Malamute, Old English Sheepdog, Siberian Husky,
    # Rottweiler
    #Intact Male 26 weeks to 156  weeks 
    elif filter_type == "MOUNTAIN":
               
                                       
        df = pd.DataFrame.from_records(db.read({
            '$or': [
                {"breed": {'$regex': re.compile(".*german.*", re.IGNORECASE) }},
                {"breed": {'$regex': re.compile(".*rott.*", re.IGNORECASE) }},
                {"breed": {'$regex': re.compile(".*malamute.*", re.IGNORECASE) }},
                {"breed": {'$regex': re.compile(".*sheepdog.*", re.IGNORECASE) }},
                {"breed": {'$regex': re.compile(".*husky.*", re.IGNORECASE) }}
            ],
            "age_upon_outcome_in_weeks": {"$gte":26.0, "$lte":156.0},
            "sex_upon_outcome": "Intact Male",} ))
    
        
                                       
    columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')
    
    return (data, columns)



# Display a pie chart about animals
#   Choice of a chart by age or breed
# 
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('chart_dropdown', 'value')])
def update_graphs(viewData, chart_dropdown):

    if( viewData == None):
        return()
    
    df = pd.DataFrame.from_dict(viewData)
     
    return [
        dcc.Graph(            
            figure = px.pie(data_frame = df,
                            names=chart_dropdown)
                            
        )    
    ]
    
#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    
    # avoid throwing an error if no row selected
    if(selected_columns == None):
        return()
    
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
    Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):  
   
    if viewData is None:
        return
    elif index is None:
        return
    
    dff = pd.DataFrame.from_dict(viewData)
    # Because we only allow single row selection, the list can be converted to a row index here
    if index is None:
        row = 0
    else: 
        row = index[0]
        
    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the grid-coordinates for the map
            # Column 4 defines the breed for the animal
            # Column 9 defines the name of the animal
            dl.Marker(position=[dff.iloc[row,13],dff.iloc[row,14]], children=[
                dl.Tooltip(dff.iloc[row,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row,9])
                ])
            ])
        ])
    ]



#app.run_server(debug=True)
# changed to app.run
#  listen for all IPs on port 8050
app.run(debug=True, host='0.0.0.0', port=8050)

