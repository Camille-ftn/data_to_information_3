# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 14:32:02 2024

@author: camil
"""

import requests
from PIL import Image
import os


os.makedirs('resultats', exist_ok=True)

chapter = 1  #
while True:
    j = 1  
    while True:
        
        pic_url = f'https://www.scan-vf.net/uploads/manga/one_piece/chapters/chapitre-{chapter}/0{j}.webp' if j < 10 else f'https://www.scan-vf.net/uploads/manga/one_piece/chapters/chapitre-{chapter}/{j}.webp'
        headers = {'user-agent': 'my-agent/1.0.1'}
        response = requests.get(pic_url, stream=True, headers=headers)
        
        
        if not response.ok:
            print(f"Chapitre {chapter} : Pas d'image trouvée pour la page {j}.")
            break  

        
        try:
            with open(f'resultats/0{j}.webp', 'wb') as file:  
                file.write(response.content)
            
            
            im = Image.open(f'resultats/0{j}.webp').convert('RGB')
            im.save(f'resultats/0{j}.png', 'png')
            print(f"Chapitre {chapter} : Image {j} téléchargée et convertie.")
        
        except Exception as e:
            print(f"Erreur lors du traitement de la page {j} du chapitre {chapter}: {e}")
            break  

        j += 1  

    break



