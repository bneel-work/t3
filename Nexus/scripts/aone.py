import os
import json
import requests
import datetime
import pandas as pd

def UpdateTokens():
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

    response = requests.get(url)
    data = response.json()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(script_dir, '..', 'configs')
    os.makedirs(config_dir, exist_ok=True)
    file_path = os.path.join(config_dir, 'aone.json')

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    return True

