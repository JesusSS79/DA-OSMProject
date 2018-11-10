#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This function wrangle the data and transform the shape of the data
into the following model. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import os

from audit_streets import update_street
from audit_phoneNumbers import update_telephone

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
ADDITIONAL_K = [ "name", "amenity", "shop", "phone", "public_transport", "capacity", "cuisine", "tourism", "natural", "information", "website", "place" ]


#function to update wrong names
def update_telephone(number):
    fix = number
    
    return fix


def shape_element(element):
    if element.tag == "node" or element.tag == "way" :
        node = {}
        created = {}
        address = {}
        node_refs = []
        
        node['type'] = element.tag
        for key,value in element.items():
            if key in CREATED:
                created[key] = value
                if not 'created' in node.keys():
                    node['created'] = created
            
            elif key == 'lat':
                if not 'pos' in node.keys():
                    node['pos'] = []
                node['pos'].insert(0, float(value))
            
            elif key == 'lon':
                if not 'pos' in node.keys():
                    node['pos'] = []
                node['pos'].insert(1, float(value))
            
            else:
                node[key] = value
        
        for value in element.iter("tag"):
            if "k" in value.attrib.keys():
                if not problemchars.match(value.attrib['k']):
                    if value.attrib['k'].find('addr:') == 0:
                        if value.attrib['k'][5:].find("street") == -1 or not "street" in address:
                            address[value.attrib['k'][5:]] = update_street(value.attrib['v'])
                        
                        if not 'address' in node.keys():
                            node['address'] = address
                    
                    elif value.attrib['k'][5:].find("phone") == -1:
                        node[value.attrib['k']] = update_telephone(value.attrib['v'])
                    elif value.attrib['k'] in ADDITIONAL_K:
                        node[value.attrib['k']] = value.attrib['v']
            
        if element.tag == "way":
            for value in element.iter("nd"):
                if "ref" in value.attrib.keys():
                    node_refs.append(value.attrib["ref"])
                    if not 'node_refs' in node.keys():
                        node['node_refs'] = node_refs
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def main():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    file = os.environ['OSMFILE']
    data = process_map(file, True)
    #pprint.pprint(data)

    
if __name__ == "__main__":
    main()