# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:54:25 2024

@author: camil
"""

import requests
import pandas as pd 

def get_worms(aphiaid):
    r = requests.get(f"https://www.marinespecies.org/rest/AphiaRecordByAphiaID/{aphiaid}")
    return r.json() if r.status_code == 200 else None

def get_worms_name(aphiaid):
    t=requests.get(f"https://www.marinespecies.org/rest/AphiaVernacularsByAphiaID/{aphiaid}")
    return t.json() if t.status_code == 200 else None


df = pd.read_excel("Table_espece_UTF8_simplifie.xlsx", "Espece_incomplet")


for index, row in df.iterrows():
    aphia = row.aphiaid_accepted
    worms_data = get_worms(aphia)
    name=get_worms_name(aphia)
    if worms_data:
        for column in df.columns:
            for k in worms_data.keys():
                if column.lower() == k.lower():
                    df.at[index, column] = worms_data[k]
                    df.at[index, "ScientificName_accepted"] = worms_data["scientificname"]
                    df.at[index, "Authority_accepted"] = worms_data["valid_authority"]
    if name and isinstance(name, list):
        for item in name:
            if item["language_code"] == "eng":
                df.at[index, "nom_commun_en"] = item["vernacular"]
            elif item["language_code"] == "fra":
                df.at[index, "nom_commun_fr"] = item["vernacular"]

df.to_excel("Table_espece_complet.xlsx", index=False)

