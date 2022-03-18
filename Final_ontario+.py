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
    # feature['geometry']['coordinates'][0]=feature['geometry']['coordinates'][0][::-1]

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

not_available_plus=[]
for item in list(city_id_map_New.keys()) :
    if item not in agg_df['CITY'].unique():
        not_available_plus.append(item)

wrong_geojson=['QUINTE WEST', 'FRONTENAC ISLANDS', 'CENTRE WELLINGTON',
'RAMARA', 'MACHIN', 'CHATHAM-KENT', 'SOUTH BRUCE PENINSULA','GREENSTONE',
 'THE NORTH SHORE', 'THE ARCHIPELAGO', 'BRANT', 'ASSIGINACK', 'TAY', 'TINY',
 'TYENDINAGA', 'RYERSON', 'STRATHROY-CARADOC', 'TEMAGAMI', 'AMHERSTBURG',
  'LAMBTON SHORES', 'TUDOR AND CASHEL']

not_available_plus=[item for item in not_available_plus if item not in wrong_geojson]


CITY_column=[]
Year=[]
SUM_CO2=[]
LOG_SUM_CO2=[]
for item in agg_df['Year'].unique():
    for CITY in not_available_plus:
 #    for CITY in ['CARLING',
 # 'WAINFLEET',
 # 'CLARENCE-ROCKLAND',
 # 'JOHNSON',
 # 'MALAHIDE',
 # 'BRETHOUR',
 # 'BRACEBRIDGE',
 # 'BRIGHTON',
 # 'HAVELOCK-BELMONT-METHUEN',
 # 'SOUTH RIVER',
 # 'POINT EDWARD',
 # 'GEORGIAN BLUFFS',
 # 'MANITOUWADGE',
 # 'BILLINGS',
 # 'BLACK RIVER-MATHESON',
 # 'OPASATIKA',
 # 'CONMEE',
 # 'CENTRAL ELGIN',
 #  'HORNEPAYNE',
 # 'THAMES CENTRE',
 # 'ELLIOT LAKE',
 # 'DEEP RIVER',
 # 'HEAD, CLARA AND MARIA',
 # 'NORTH ALGONA WILBERFORCE',
 # 'PERRY',
 # 'WHITCHURCH-STOUFFVILLE',
 # 'OWEN SOUND',
 # 'COLEMAN',
 # 'TRENT LAKES',
 # 'MATTAWAN',
 # 'BROCK',
 # 'SIOUX NARROWS-NESTOR FALLS',
 # 'EAST HAWKESBURY',
 # 'LAKE OF BAYS',
 # 'LARDER LAKE',
 #  'HORTON',
 # 'CHISHOLM',
 # 'BROCKTON',
 # 'PRINCE',
 # 'JOLY',
 # 'GEORGIAN BAY',
 # 'SOUTH STORMONT',
 # 'PLUMMER ADDITIONAL',
 # 'THORNLOE',
 # 'LEEDS AND THE THOUSAND ISLANDS',
 # 'NIPISSING',
 # 'UXBRIDGE',
 # 'OTONABEE-SOUTH MONAGHAN',
 # 'ALBERTON',
 # 'BURPEE AND MILLS',
 # 'JOCELYN',
 # 'DUTTON/DUNWICH',
 # 'GORDON / BARRIE ISLAND',
 # 'KAWARTHA LAKES',
 # 'ATHENS',
 # 'KINCARDINE',
 # 'MCKELLAR',
 # 'CENTRE HASTINGS',
 # 'TEMISKAMING SHORES',
 # 'SOUTH FRONTENAC',
 # 'GRAVENHURST',
 # 'RED ROCK',
 #  'TAY VALLEY',
 # 'MERRICKVILLE-WOLFORD',
 # 'ADDINGTON HIGHLANDS',
 # 'GANANOQUE',
 # 'WARWICK',
 # 'NORWICH',
 # 'PETROLIA',
 # 'SABLES-SPANISH RIVERS',
 # 'LAIRD',
 # 'ORILLIA',
 # 'BRADFORD WEST GWILLIMBURY',
 # 'MORLEY',
 # 'NORFOLK COUNTY',
 # 'BARRIE',
 # 'MEAFORD',
 # 'RAINY RIVER',
 #  'LA VALLEE',
 # 'LAURENTIAN HILLS',
 # 'WEST ELGIN',
 # 'LOYALIST',
 # 'CHATSWORTH',
 # 'MCDOUGALL',
 # 'WASAGA BEACH',
 # 'CHAMPLAIN',
 # 'HARRIS',
 # 'NORTH FRONTENAC',
 # 'KING',
 # 'ST. CLAIR',
 # 'NORTH KAWARTHA',
 # 'MCNAB/BRAESIDE',
 # 'BONFIELD',
 # 'ORO-MEDONTE',
 # 'KILLARNEY',
 # 'ST. JOSEPH',
 # 'BECKWITH',
 # 'HIGHLANDS EAST',
 # 'CHAPPLE',
 # 'MCGARRY',
 # 'SOUTH GLENGARRY',
 # 'BRUDENELL, LYNDOCH AND RAGLAN',
 # 'MIDLAND',
 # 'ST.-CHARLES',
 # 'CRAMAHE',
 # 'LAURENTIAN VALLEY',
 # 'MUSKOKA LAKES',
 # 'ARNPRIOR',
 # 'SOUTHWOLD',
 # 'ARRAN-ELDERSLIE',
 # 'SOUTHGATE',
 # 'BANCROFT',
 # 'MACDONALD, MEREDITH AND ABERDEEN ADDITIONAL',
 # 'MELANCTHON',
 # "BURK'S FALLS",
 # 'CLARINGTON',
 # 'NEWBURY',
 # 'GEORGINA',
 #  'SOUTH HURON',
 # 'DYSART, DUDLEY, HARCOURT, GUILFORD, HARBURN, BRUTO',
 # 'HUDSON',
 # 'AJAX',
 # 'STRONG',
 # 'CENTRAL FRONTENAC',
 # 'NORTHERN BRUCE PENINSULA',
 #  'NORTHEASTERN MANITOULIN AND THE ISLANDS',
 # 'GILLIES',
 # 'NORTH DUMFRIES',
 # 'TWEED',
 # 'SOUTHWEST MIDDLESEX',
 #  'DESERONTO',
 # 'MONO',
 # 'WELLINGTON NORTH',
 # 'AUGUSTA',
 #  'MISSISSIPPI MILLS',
 # 'LUCAN BIDDULPH',
 # 'BRUCE MINES',
 # 'JAMES',
 # 'MAPLETON',
 # 'HASTINGS HIGHLANDS',
 # 'CASEY',
 # 'MACHAR',
 # 'OIL SPRINGS',
 # 'MARATHON',
 # 'SHUNIAH',
 # 'SEVERN',
 # 'CALVIN',
 #  'FAUQUIER-STRICKLAND',
 # 'INNISFIL',
 # 'WHITEWATER REGION',
 # 'CAVAN MONAGHAN',
 # 'ENNISKILLEN',
 # 'BALDWIN',
 # 'LASALLE',
 #  'STIRLING-RAWDON',
 # 'SOUTH ALGONQUIN',
 # 'WILMOT',
 # 'MULMUR',
 # 'NEW TECUMSETH',
 # 'HURON SHORES',
 # 'BAYHAM',
 # 'CENTRAL MANITOULIN',
 # 'PELHAM',
 # 'DOURO-DUMMER',
 # 'FRENCH RIVER',
 # 'HILTON BEACH',
 # 'ALFRED AND PLANTAGENET',
 # 'RENFREW',
 # 'ADJALA-TOSORONTIO',
 # 'PARRY SOUND',
 # 'PERTH',
 # 'MATTICE-VAL CÃ”TÃ‰',
 # 'NEEBING',
 # 'ALNWICK/HALDIMAND',
 # 'MAGNETAWAN',
 # 'MARMORA AND LAKE',
 # 'HOWICK',
 # 'MOOSONEE',
 # 'OLIVER PAIPOONGE',
 # 'PUSLINCH',
 # 'TRENT HILLS',
 # 'NAIRN AND HYMAN',
 # 'CENTRAL HURON',
 # 'ASHFIELD-COLBORNE-WAWANOSH',
 # 'PAPINEAU-CAMERON',
 # 'AMARANTH',
 # 'ARMOUR',
 # 'MINDEN HILLS',
 # 'COBALT',
 # 'ERIN',
 # 'GRAND VALLEY',
 # 'HURON-KINLOSS',
 # 'CHAMBERLAIN',
 # 'MINTO',
 # 'ADELAIDE-METCALFE',
 # 'HARLEY',
 # 'SOUTH DUNDAS',
 # 'THE BLUE MOUNTAINS',
 # 'GAUTHIER',
 # 'NORTH DUNDAS',
 # 'BLANDFORD-BLENHEIM',
 # 'MARKSTAY-WARREN',
 # 'TECUMSEH',
 # 'CALEDON',
 #  'AURORA',
 # 'KEARNEY',
 # 'NORTH GRENVILLE',
 # 'WEST GREY',
 # 'LATCHFORD',
 # 'GORE BAY',
 # 'PENETANGUISHENE',
 # 'ARMSTRONG',
 # 'CALLANDER',
 # 'NORTH MIDDLESEX',
 # 'DORION',
 # 'SIOUX LOOKOUT',
 # 'SCUGOG',
 # 'LIMERICK',
 # 'EDWARDSBURGH/CARDINAL',
 #  'MATTAWA',
 # 'HANOVER',
 # 'SCHREIBER',
 # 'NORTH PERTH',
 # 'THESSALON',
 # 'SMITHS FALLS',
 # 'ESSA',
 # 'IGNACE',
 # 'PELEE',
 # 'ALGONQUIN HIGHLANDS',
 # 'SPANISH',
 # 'BONNECHERE VALLEY',
 # 'NORTH STORMONT',
 # 'TARBUTT',
 # 'MADAWASKA VALLEY',
 # 'FRONT OF YONGE',
 # 'GREY HIGHLANDS',
 # 'DAWSON',
 # 'WELLESLEY',
 # 'NIAGARA-ON-THE-LAKE',
 # 'SAUGEEN SHORES',
 # 'NORTH GLENGARRY',
 # 'CHARLTON AND DACK',
 # 'TEHKUMMAH',
 # 'HILTON',
 # 'SMOOTH ROCK FALLS',
 # 'ASPHODEL-NORWOOD',
 # 'KERNS',
 # 'WOLLASTON',
 # 'SUNDRIDGE',
 # 'VAL RITA-HARTY',
 # "O'CONNOR",
 # 'WOOLWICH',
 # 'WHITE RIVER',
 # 'GREATER MADAWASKA',
 # 'ADMASTON/BROMLEY',
 # 'MCMURRICH/MONTEITH',
 # 'GREATER SUDBURY',
 # 'CARLOW/MAYO',
 #  'SHELBURNE',
 # 'STONE MILLS',
 # 'WESTPORT',
 # 'PERTH SOUTH',
 # 'ZORRA',
 # 'MORRIS-TURNBERRY',
 # 'SOUTH-WEST OXFORD',
 # 'HURON EAST',
 # 'NORTH HURON',
 # 'EAST FERRIS',
 # 'ELIZABETHTOWN-KITLEY',
 # 'PRINCE EDWARD',
 # 'CARLETON PLACE',
 # 'KILLALOE, HAGARTY AND RICHARDS',
 # 'FARADAY',
 # 'CHAPLEAU',
 # 'LINCOLN',
 # 'PLYMPTON-WYOMING',
 # 'ORANGEVILLE',
 # 'LAKE OF THE WOODS',
 # 'BLUEWATER',
 # 'RIDEAU LAKES',
 # 'WEST NIPISSING',
 # 'BROOKE-ALVINSTON',
 # 'HILLIARD',
 # 'POWASSAN',
 # 'SELWYN',
 # 'MONTAGUE',
 # 'LANARK HIGHLANDS',
 # 'PICKLE LAKE',
 # 'THE NATION',
 # 'SEGUIN',
 # 'DRUMMOND/NORTH ELMSLEY',
 # 'COCKBURN ISLAND',
 # 'WEST PERTH',
 # 'MIDDLESEX CENTRE',
 # 'EVANTUREL',
 # 'COBOURG',
 # 'EAST GWILLIMBURY',
 # 'SOUTH BRUCE',
 # 'CLEARVIEW',
 # 'EAST GARAFRAXA',
 # 'CASSELMAN',
 # 'EAST ZORRA-TAVISTOCK',
 # 'PERTH EAST',
 # 'EAR FALLS',
 # 'RUSSELL',
 # 'TILLSONBURG',
 # 'WHITESTONE',
 # 'DAWN-EUPHEMIA',
 # 'MOONBEAM',
 # 'GUELPH/ERAMOSA',
 # 'SPRINGWATER',
 # 'RICHMOND HILL']:
        Year.append(item)
        CITY_column.append(CITY)
        SUM_CO2.append(1)



agg_df_plus=pd.DataFrame()
agg_df_plus['Year']=Year
agg_df_plus['CITY']=CITY_column
agg_df_plus['SUM_CO2']=SUM_CO2
agg_df_plus['LOG_SUM_CO2']=np.log10(agg_df_plus['SUM_CO2'])
agg_df_plus['id']=agg_df_plus['CITY'].apply(lambda x:city_id_map_New[x])

for feature in obj_Ontario['features']:
    feature['geometry']['coordinates'][0]=feature['geometry']['coordinates'][0][::-1]

# for feature in obj_Ontario['features']:
#     if feature['properties']['MUNICIPAL_NAME_SHORTFORM'] in wrong_geojson:
#         feature['geometry']['coordinates'][0]=feature['geometry']['coordinates'][0][::-1]

agg_final=pd.concat([agg_df,agg_df_plus])
# agg_final=agg_df
# agg_final=agg_df_plus


app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Year:"),
    dcc.Slider(agg_final['Year'].unique().min(),agg_final['Year'].unique().max(),
               value=agg_final['Year'].unique().max(),step=None,
               marks={str(year):str(year) for year in agg_final['Year'].unique()},id='year'),
    dcc.Graph(id="graph_with_slider"),
])

@app.callback(
    Output("graph_with_slider", "figure"),
    Input("year", "value"))

def display_choropleth(year):
    filtered_agg_df=agg_final[agg_final['Year']==year]
    fig = px.choropleth(
        filtered_agg_df, geojson=obj_Ontario, color='LOG_SUM_CO2',
        hover_name='CITY',locations="id",color_continuous_scale="Turbo")
    # fig = px.scatter_geo(
    #     filtered_agg_df, geojson=obj_Ontario,size='SUM_CO2',
    #     hover_name='CITY',locations="id",
    #     color_continuous_scale="Blues")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    annotations = [dict(
        x=0,
        y=0,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://data.ontario.ca/dataset/da0bd7d1-1591-4dcd-8d68-b3882cad31b2">\
            Greenhouse gas emissions reporting by facility_Ontario</a>',
        showarrow = False
    )])

    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(use_reloader=False)
