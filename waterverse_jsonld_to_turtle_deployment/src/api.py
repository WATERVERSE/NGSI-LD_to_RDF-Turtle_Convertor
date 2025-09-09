"""
@Author: TessaVrijhoeven
@Date: October 16, 2024

Using this script one can run the json_to_ttl converter
by running convert_request_to_turtle().

This service was developed as part of the Horizon Europe Project Waterverse,
with a Grant agreement ID: 101070262
"""

import requests
from flask import Flask, Response, request, jsonify
from io import StringIO
from rdflib import Graph
from rdflib.tools.rdf2dot import rdf2dot
from graphviz import Source
from json_to_ttl_convertor import jsontoturtle
import logging

# # only import examples if the script is ran locally 
# from json_to_ttl.examples import file_path_json_ld, destination_of_converted_file, destination_png

def convert_request_to_turtle(json_file, destination=None, to_save=False):
    """
    Function that uses the jsontoturtle() to convert the json-ld file to ttl syntax if
    no desitination is specified and to_save=False. When to_save=True and a destination
    is given the ttl syntax will be saved in a .ttl file
    """
    return jsontoturtle(json_file, destination, to_save)
   
def visualization_ttl(ttl_file, destination):
    """
    Function that reads the ttl file, converts it to a dot-string
    and uses Graphviz to visualize the rdf graph
    """
    g=Graph()
    g.parse(ttl_file, format='ttl')

    dot_ouput_stream=StringIO()
    rdf2dot(g, stream=dot_ouput_stream)
    dot_representation=dot_ouput_stream.getvalue()

    graph=Source(dot_representation, format='dot')

    graph.render(destination, format='png', cleanup=True)

app=Flask(__name__)

@app.route('/test')
def test():
    """
    Serves as a quick test to see whether the API
    is working correctly. 
    """
    return jsonify('API call successful')

@app.route('/json_to_ttl', methods=['post'])
def process_request():
    """
    The primary JSON-LD to turtle converter function 
    where the convert_request_to_turtle function is
    called. This function is the endpoint where 
    JSON-LD data posted to 'ipadress/json_to_ttl' is
    routed to, to allow for the conversion to turtle.
    Returns
    -------
    """
    try:
        data_json=request.get_json()
        if data_json:
            logging.info(f'Received JSON-LD: {data_json}')
        else:
            logging.warning(f'The JSON-LD has not been received!')
            
        try:
            result_ttl=convert_request_to_turtle(data_json)
            logging.info(f"Successfully converted JSON-LD to Turtle-syntax: {result_ttl}")
        
        except Exception as e:
           logging.warning(f'Unfortunately the conversion is not working! {e}')
           return jsonify("")

    except Exception as e:
        logging.warning(f'The request is could not be processed!')
        return jsonify("")

    return Response(result_ttl, content_type='text/turtle', status=200)

if __name__ == '__main__':
    # define the JSON-LD file, destination of converted ttl file and for the graphic created in
    # the __init__ file
    ttl_syntax = convert_request_to_turtle(file_path_json_ld)
    convert_request_to_turtle(file_path_json_ld, destination=destination_of_converted_file,
                              to_save=True)
    # visualization_ttl(destination_of_converted_file, destination_png)
    print(ttl_syntax)
