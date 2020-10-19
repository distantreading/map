# Script for creating a map of the members shown in the tsv-file using the library folium.

import folium
from folium import plugins
import numpy as np
import pandas as pd
import geocoder
import requests
import re

# create basic map
start_adress = geocoder.osm("Trier, Germany")
start_a_latlng = [start_adress.lat, start_adress.lng]
m = folium.Map(start_a_latlng, zoom_start = 4)

# get all members, incl city (use geocoder for lat and long) and working group
# read as dataframe
with open("action-members-wgs.tsv", "r", encoding="utf8") as infile:
    members = pd.read_csv(infile, sep="\t")

members = members.drop(columns=["Unnamed: 0"])
print(members)

# get all cities for map
cities = members["city"].dropna().tolist()
cities = set(cities)
#print(cities)
# get all members within a city
for c in cities:
    city_list = []
    for ind, row in members.iterrows():
        if c == row["city"]:
            city_list.append(row["name"] + ": " +  row["WG"])
    #print(city_list)
    try:
        adress = geocoder.osm(c)
        adress_latlng = [adress.lat, adress.lng]
        popup = folium.Popup('<br>'.join(city_list), max_width = 300, min_width=100)
        folium.Marker(adress_latlng, popup = popup , tooltip = c).add_to(m) #[str(m + "\n") for m in city_list]
    except ValueError:
        print(c)

m.save("action-map.html")
