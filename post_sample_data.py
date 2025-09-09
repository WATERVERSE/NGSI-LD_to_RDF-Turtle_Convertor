"""
@Author: TessaVrijhoeven, researcher at KWR Water Research Institute
@Date: December 5, 2024

This script is a test way to interact/ultilise the json_to_ttl
converter with an API enpoint of the Docker.

This service was developed as part of the Horizon Europe Project Waterverse,
with a Grant agreement ID: 101070262
"""

import requests
import json
import logging
from examples import file_path_json_ld


# load the JSON-LD in a variable
with open(file_path_json_ld, 'r', encoding='utf-8') as f:
    json_test=json.load(f)

# post the JSON-LD to the API in the Docker to convert the JSON-LD to Turtle-syntax
response=requests.post(url=f'http://localhost:80/json_to_ttl',
                       headers={'Content-Type':'application/json',
                                'Accept': 'text/turtle'},
                       json=json_test)

logging.info(f'The response is {response}')

# if a response is received, extract the data of the response (the Turtle-syntax)
if response.status_code == 200:
    response_data = response.text
    print("Received response", response_data)
else:
    print("Failed to receive response. Statue code: ", response.status_code)