#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Iterative parsing to process the map file and find out not only what tags are there, 
but also how many, to get the feeling on how much of which data you can expect to have in the map.
"""
import xml.etree.cElementTree as ET
import pprint
import os

OSMFILE = "LaPalma.osm"

def count_tags(filename):
    tags = {}
    
    tree = ET.parse(filename)
    root = tree.getroot()
    for elto in root.iter():
        if not elto.tag in tags:
            tags[elto.tag] = 1
        else:
            tags[elto.tag] += 1  
    
    return tags

def main():
    file = os.environ['OSMFILE']
    tags = count_tags(file)
    pprint.pprint(tags)

if __name__ == "__main__":
    main()