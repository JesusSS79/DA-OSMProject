#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Iterative parsing to process the map file and find out the attributes "highway" and "tracktype" 
in order to analyse the quality of the classification of the ways.
"""
import xml.etree.cElementTree as ET
import pprint
import os

def count_tags(filename):
    tags = {"way": 0, "highway": 0, "tracktype": 0}
    
    tree = ET.parse(filename)
    root = tree.getroot()
    for elto in root.iter():
        if elto.tag == "way":
            tags['way'] += 1
            for wayElto in elto.iter():
                if wayElto.tag == "tag":
                    for elt in wayElto.items():
                        if elt[0] == 'k' and elt[1] == 'highway':
                            tags['highway'] += 1
                        if elt[0] == 'k' and elt[1] == 'tracktype':
                            tags['tracktype'] += 1    
    
    return tags

def main():
    file = os.environ['OSMFILE']
    tags = count_tags(file)
    pprint.pprint(tags)

if __name__ == "__main__":
    main()