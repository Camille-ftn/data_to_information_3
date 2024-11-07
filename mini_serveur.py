# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 08:24:59 2024

@author: camil
"""

from flask import Flask, render_template, request
import pandas as pd 
import requests
import folium
from folium.plugins import MarkerCluster
import xyzservices

app=Flask(__name__)

global port

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/moi')
def me():
    return 'Hello, Camille!'

@app.route('/data')
def serv_data():
    r=df.to_json(orient='records')
    return r

@app.route('/data_template')
def tableau():
    return render_template('exported_data.html')

def get_data():
    r=requests.get("http://data.portic.fr/api/ports?param=&shortenfields=false&both_to=false&date=1787")
    r=r.json()
    df=pd.DataFrame(r)
    return df

def create_map(param1,param2):
        
    default_location = (46.16308, -1.15222)
    location = default_location
    
    if param1 in port.admiralty:
        location=port.admiralty[param1]
    
    filt=port
    if param2 != None:
        filt=port[port.state_1789_fr == param2]
        
    smithsonian_provider = xyzservices.TileProvider (name="Stamen maps, hosted by Smithsonian",
                                                     url="https://watercolormaps.collection.cooperhewitt.org/tile/watercolor/{z}/{x}/{y}.jpg",
                                                     attribution="(C) Stamen Design",)
    
    svg_boat_fr = '''<svg xmlns="http://www.w3.org/2000/svg" height="24" width="27" viewBox="0 0 576 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#171593" d="M320 96a32 32 0 1 1 -64 0 32 32 0 1 1 64 0zm21.1 80C367 158.8 384 129.4 384 96c0-53-43-96-96-96s-96 43-96 96c0 33.4 17 62.8 42.9 80L224 176c-17.7 0-32 14.3-32 32s14.3 32 32 32l32 0 0 208-48 0c-53 0-96-43-96-96l0-6.1 7 7c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9L97 263c-9.4-9.4-24.6-9.4-33.9 0L7 319c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l7-7 0 6.1c0 88.4 71.6 160 160 160l80 0 80 0c88.4 0 160-71.6 160-160l0-6.1 7 7c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-56-56c-9.4-9.4-24.6-9.4-33.9 0l-56 56c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l7-7 0 6.1c0 53-43 96-96 96l-48 0 0-208 32 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-10.9 0z"/></svg>'''

    svg_boat_autre = '''<svg xmlns="http://www.w3.org/2000/svg" height="24" width="27" viewBox="0 0 576 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#931515" d="M320 96a32 32 0 1 1 -64 0 32 32 0 1 1 64 0zm21.1 80C367 158.8 384 129.4 384 96c0-53-43-96-96-96s-96 43-96 96c0 33.4 17 62.8 42.9 80L224 176c-17.7 0-32 14.3-32 32s14.3 32 32 32l32 0 0 208-48 0c-53 0-96-43-96-96l0-6.1 7 7c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9L97 263c-9.4-9.4-24.6-9.4-33.9 0L7 319c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l7-7 0 6.1c0 88.4 71.6 160 160 160l80 0 80 0c88.4 0 160-71.6 160-160l0-6.1 7 7c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-56-56c-9.4-9.4-24.6-9.4-33.9 0l-56 56c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l7-7 0 6.1c0 53-43 96-96 96l-48 0 0-208 32 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-10.9 0z"/></svg>'''
    m=folium.Map(location=location,tiles=smithsonian_provider,zoom_start=10)
    marker_cluster = MarkerCluster().add_to(m)
    group_1=folium.FeatureGroup("ports").add_to(m )
    for index, row in filt.iterrows():
        folium.Marker(
            location=[row.y, row.x],
            tooltip=row.toponym,
            popup=row.admiralty,
            icon=folium.DivIcon(html=svg_boat_fr if row.state_1789_fr=="France" else svg_boat_autre),
        ).add_to(marker_cluster)
    folium.LayerControl().add_to(m)
    return m

@app.route('/carte_template')
def map_port():
    country = request.args.get("pays")
    filt = port 
    if country != None:
        # Filtrer le dataframe sur le pays
        filt = port[port.state_1789_fr == country]
    
    m = create_map("La Rochelle",country)
    return render_template('portic_map.html', msg=m.get_root()._repr_html_(), y =filt.to_html())

if __name__=='__main__':
    df=pd.read_excel("data for analyses_2010_2011_analyses.xls",sheet_name="data for analyses_2010_2011_ana")
    port =get_data()
    app.run(port=5050)
