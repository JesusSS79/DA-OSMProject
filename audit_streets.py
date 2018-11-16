#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This function perform the following steps:
- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import os

street_type_re = re.compile(r'^\S+\b', re.IGNORECASE)

expected = ["Calle", "Carretera", "Avenida", "Camino", "Barrio", "Lugar", "Finca", "Llano", "La", "Las", "El", "Pared", "Callejón", "Hoyo", "Lomada", "Pino", "Playa", "Plaza", "Tierras", "Travesia", "Urbanización", "Centro", "Mirca", "Paseo", "Pista"]

# UPDATE THIS VARIABLE
mapping = { "C\\": "Calle",
            "C/": "Calle",
            "CALLE": "Calle",
            "calle": "calle",
            "CARRETERA": "Carretera",
            "carretera": "Carretera",
            "8Ctra": "Carretera",
            "camino": "Camino",
            "Avda.": "Avenida",
            "Avda": "Avenida",
            "Ctra.": "Carretera",
            "Ctra": "Carretera",
            "Crta.": "Carretera",
            "Crta": "Carretera",
            "Created.": "Carretera",
            "Urbanizacón": "Urbanización",
            "Urbanizacion": "Urbanizacion"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_street(name):
    fix = name
    replaces = set()
    for key, value in mapping.items():
        if key in name:
            replaces.add(key)
   
    if (len(replaces) > 0):  
        replaceKey = sorted(replaces, reverse=True)
        fix = name.replace(replaceKey[0], mapping[replaceKey[0]])
    
    return fix


def main():
    file = os.environ['OSMFILE']
    st_types = audit(file)

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_street(name)
            if (name != better_name):
                print (name, "=>", better_name)

if __name__ == '__main__':
    main()