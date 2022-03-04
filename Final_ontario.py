import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as sm
import requests
import json
import plotly.express as px
import dash
import pickle


from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.metrics import r2_score
from sklearn.linear_model import LassoCV,RidgeCV
from sklearn.metrics import confusion_matrix
from collections import ChainMap


from scipy import stats
import statsmodels.api as sm

df=pd.read_csv('GHG_Data_2010_2019_data_Dec172020.csv')

City=df['Facility City'].unique()

with open ("Municipal_Boundary_-_Lower_and_Single_Tier.geojson",'r') as geo_file:
    obj_Ontario=json.load(geo_file)

city_id_map_New={}
for feature in obj_Ontario['features']:
    feature['id']=feature['properties']['MUNID']
    city_id_map_New[feature['properties']['MUNICIPAL_NAME_SHORTFORM']]=feature['id']
    feature['geometry']['coordinates'][0]=feature['geometry']['coordinates'][0][::-1]

df['Facility City_upper']=df['Facility City'].str.upper()

df.dropna(subset=['Facility City_upper'],inplace=True)

not_available=[]
for item in City:
    item=str(item).upper()
    if item not in list(city_id_map_New.keys()):
        not_available.append(item)

df_revised_plus=df[~df['Facility City_upper'].isin (not_available)]

df_revised_plus['id']=df_revised_plus['Facility City_upper'].apply(lambda x:city_id_map_New[x])

# df_revised_plus['log_Reporting Amount in CO2e (t)']=np.log10(df_revised_plus['Reporting Amount in CO2e (t)'])

# NEW_Agg_MAP={}
# list_year=[]
# for year in df_revised_plus['Year']:
#     for CITY in df_revised_plus['Facility City_upper']:
#         NEW_Agg_MAP[f"{CITY}-{year}"]=df_revised_plus[(df_revised_plus['Year']==year) & (df_revised_plus['Facility City_upper']==CITY)]['Reporting Amount in CO2e (t)'].sum()

a_file = open("NEW_Agg_MAP.pkl", "rb")
NEW_Agg_MAP = pickle.load(a_file)

sum_final=list(NEW_Agg_MAP.values())

year=[]
cities=[]
for item in list(NEW_Agg_MAP.keys()):
    year.append(item.split("-")[1])
    cities.append(item.split("-")[0])

year = list(map(int, year))
w=[]
agg_df=pd.DataFrame(w)

agg_df['Year']=year
agg_df['CITY']=cities
agg_df['SUM_CO2']=sum_final
agg_df['LOG_SUM_CO2']=np.log10(agg_df['SUM_CO2'])

agg_df['id']=agg_df['CITY'].apply(lambda x:city_id_map_New[x])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Year:"),
    dcc.Slider(agg_df['Year'].unique().min(),agg_df['Year'].unique().max(),
               value=agg_df['Year'].unique().max(),step=None,
               marks={str(year):str(year) for year in agg_df['Year'].unique()},id='year'),
    dcc.Graph(id="graph_with_slider"),
])

@app.callback(
    Output("graph_with_slider", "figure"),
    Input("year", "value"))

def display_choropleth(year):
    filtered_agg_df=agg_df[agg_df['Year']==year]
    fig = px.choropleth(
        filtered_agg_df, geojson=obj_Ontario, color='LOG_SUM_CO2',
        hover_name='CITY',locations="id")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(use_reloader=False)
