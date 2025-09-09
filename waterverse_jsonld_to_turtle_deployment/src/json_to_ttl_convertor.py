"""
@Author: TessaVrijhoeven, researcher at KWR Water Research Institute
@Date: October 16, 2024

This script contains functions to convert JSON-LD input into ttl-syntax.
That is, a function that uses the parse and serialize functions of the rdflib 
library to convert an input JSON-LD into the corresponding ttl-syntax, and a
seperate function that checks the @context of the input JSON-LD file to
ensure that the JSON-LD file contains the correct context.

This service was developed as part of the Horizon Europe Project Waterverse,
with a Grant agreement ID: 101070262
"""

import json
import logging
import re
from rdflib import Graph
import logging

def model_extraction(context_string):
    """
    Function that extracts the type of dataModel.
    This function is used to check the context
    """
    match = re.search(r"/dataModel\.(\w+)/", context_string)
    data_model=match.group(1) if match else None
    return data_model

def context_check(jsonld_data):
    """
    Function that checks whether the @context in the JSON-LD input
    is correct, i.e. a 'smart-data-models.github.io'-url. If not the
    context is overwritten by the correct one.
    """

    logging.info(f'A context check is performed on: {jsonld_data}')

        #store @context in variable for dict-type json-ld input
    if isinstance(jsonld_data, dict):
        logging.info('JSON-LD data is a dict')
        if '@context' in jsonld_data:
            context=jsonld_data['@context']
            context_url=context[0]
            #search for data model type based on url in context
            model=model_extraction(context_url)
            # replace @context-URL if not correct
            if context_url == f'https://smart-data-models.github.io/dataModel.{model}/context.jsonld':
                context.append('https://smartdatamodels.org/context.jsonld')
                jsonld_data['@context']=context
            else:
                jsonld_data['@context']=[f'https://smart-data-models.github.io/dataModel.{model}/context.jsonld', 'https://smartdatamodels.org/context.jsonld']
            logging.info(f'JSON-LD after context check: {jsonld_data}')
            return jsonld_data        
        #if the json-ld contains a list of dicts inside a dict:
        #go through this list and store @context in variable   
        else:
            for _, item in enumerate(jsonld_data):
                data=jsonld_data[item]
                if isinstance(data, list):
                    logging.info('JSON-LD data is a dict containing a list of dictionaries')
                    for _, item in enumerate(data):
                        context=item.get('@context')
                        context_url=context[0]
                        #search for data model based on url in context
                        model=model_extraction(context_url)
                        # replace @context-URL if not correct
                        if context_url == f'https://smart-data-models.github.io/dataModel.{model}/context.jsonld':
                            context.append('https://smartdatamodels.org/context.jsonld')
                            item['@context']=context
                        else:
                            item['@context']=[f'https://smart-data-models.github.io/dataModel.{model}/context.jsonld', 'https://smartdatamodels.org/context.jsonld']
                logging.info(f'JSON-LD after context check: {data}')
                return data
                            
    #store @context in variable for 'list of dict'-type json-ld
    if isinstance(jsonld_data, list):
        logging.info('JSON-LD data is a list of dictionaries')
        for _, item in enumerate(jsonld_data):
            context=item.get('@context')
            context_url=context[0]
            #search for data model based on url in context
            model=model_extraction(context_url)
            # replace @context-URL if not correct
            if context_url == f'https://smart-data-models.github.io/dataModel.{model}/context.jsonld':
                context.append('https://smartdatamodels.org/context.jsonld')
                item['@context']=context
            else:
                item['@context']=[f'https://smart-data-models.github.io/dataModel.{model}/context.jsonld', 'https://smartdatamodels.org/context.jsonld']
        logging.info(f'JSON-LD after context check: {jsonld_data}')
        return jsonld_data

def jsontoturtle(jsonld, destination=None, to_save=False):
    """
    Function that converts the json-ld (with correct @context) to ttl syntax.
    'destination' and 'to_save' allow for saving as a ttl-file. For deployement
    the ttl syntax will be returned.
    """

    jsonld_cor_context=context_check(jsonld)

    #convert the json-ld dict to a json-formatted string
    try:
        json_string =json.dumps(jsonld_cor_context)
    except Exception as e:
        logging.warning('The provided JSON-LD file cannot be converted to a JSON-formatted string '
                        'due to exception: %s. Please check your input', e)
        return
 
    bytes_object =json_string.encode('utf-8')

    #create an RDF graph with common namespaces
    g=Graph(bind_namespaces='rdflib')
           
    #load the json-ld file into the graph
    g.parse(bytes_object, format='json-ld')
  
    if to_save:
    #serialize and save as ttl file
        g.serialize(destination, format='ttl')

    else:
    #access the serialized ttl data from the graph and store the it in a variable
        ttl_string=g.serialize(format='ttl')

        #textual changes based on end user preference
        if ttl_string.find(' a '):
            ttl_string=ttl_string.replace(' a ', ' rdf:type ').replace('@prefix', 'PREFIX')
        logging.info(f'The ttl-conversion is completed, resulting ttl-syntax: {ttl_string}')
        return ttl_string
