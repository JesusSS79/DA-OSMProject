#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
There are 3 regular expressions to check for certain patterns in the tags.
The function count of each of four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
"""
import xml.etree.cElementTree as ET
import pprint
import re
import os

lower = re.compile(r'^[a-z]*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*[a-z]+$')
lower_several_colon = re.compile(r'^([a-z]|_|:)*[a-z]+$')
problemchars = re.compile(r'.*[=\+/&<>;\'"\?%#$@\,\. \t\r\n].*')
some_hyphen = re.compile(r'.*-.*')
some_upper = re.compile(r'.*[A-Z].*')
some_number= re.compile(r'.*[0-9].*')

def key_type(element, keys):
    processedKeys = []
    
    if element.tag == "tag":
        for elt in element.items():
            if elt[0] == 'k' and not elt[1] in processedKeys:
                processedKeys.append(elt[1])
                if lower.match(elt[1]):
                    keys['lower'] += 1
                elif lower_colon.match(elt[1]):
                    keys['lower_colon'] += 1
                elif lower_several_colon.match(elt[1]):
                    keys['lower_several_colon'] += 1
                elif problemchars.match(elt[1]):
                    keys['problemchars'] += 1
                elif some_hyphen.match(elt[1]):
                    keys['some_hyphen'] += 1
                elif some_number.match(elt[1]):
                    keys['some_number'] += 1
                elif some_upper.match(elt[1]):
                    keys['some_upper'] += 1
                else:
                    keys['other'] += 1
                    
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "lower_several_colon": 0, "problemchars": 0, "some_hyphen": 0, "some_number": 0, "some_upper": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


def main():
    file = os.environ['OSMFILE']
    keys = process_map(file)
    pprint.pprint(keys)

if __name__ == "__main__":
    main()