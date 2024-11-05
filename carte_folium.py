# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 08:57:41 2024

@author: camil
"""

import requests
import pandas as pd 
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import xyzservices

r=requests.get("http://data.portic.fr/api/ports?param=&shortenfields=false&both_to=false&date=1787")
r=r.json()
df=pd.DataFrame(r)
df.admiralty
pd.unique(df.admiralty)
len(pd.unique(df.admiralty))
pd.unique(df.state_1789_fr)
len(pd.unique(df.state_1789_fr))

val={'admiralty':'X','state_1789_fr':'UNKNOWN'}
df=df.fillna(value=val)
df.admiralty.isnull().values.any()
df.state_1789_fr.isnull().values.any()

res=df.groupby('admiralty')['ogc_fid'].count()
print(res)

res_state=df.groupby('state_1789_fr')['ogc_fid'].count()
print(res_state)


smithsonian_provider = xyzservices.TileProvider (name="Stamen maps, hosted by Smithsonian",
                                                 url="https://watercolormaps.collection.cooperhewitt.org/tile/watercolor/{z}/{x}/{y}.jpg",
                                                 attribution="(C) Stamen Design",)

m=folium.Map(location=(46.16308,-1.15222),tiles=smithsonian_provider,zoom_start=4)
marker_cluster = MarkerCluster().add_to(m)
group_1=folium.FeatureGroup("ports").add_to(m )
for index, row in df.iterrows():
    folium.Marker(
        location=[row.y, row.x],
        tooltip=row.toponym,
        popup=row.admiralty,
        icon=folium.Icon(color="blue" if row.state_1789_fr=="France" else "red"),
    ).add_to(marker_cluster)
folium.LayerControl().add_to(m)
m.save("carte.html")
