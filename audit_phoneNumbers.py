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

phoneNumber_type_re = re.compile(r'^\+34[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$')

def audit_telephone_type(telephone_types, telephone_number):
    if not phoneNumber_type_re.match(telephone_number):
        telephone_types.add(telephone_number)


def is_telephone(elem):
    return elem.attrib['k'] == "phone"


def audit(osmfile):
    osm_file = open(osmfile, "r")
    telephone_types = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_telephone(tag):
                    audit_telephone_type(telephone_types, tag.attrib['v'])
    osm_file.close()
    return telephone_types


def update_telephone(name):
    fix = name.replace("Tel.:","")
    fix = fix.replace("-","")
    fix = fix.replace(" ","")
    fix = fix.replace(".","")
    fix = fix.replace("(","")
    fix = fix.replace(")","")
    fix = fix.replace(".","")
    fix = fix.replace("/","")
    if len(fix) == 9:
        fix = "+34"+fix
    if fix.startswith('0034'):
        fix = "+34"+fix[4:]
    
    #Custom double telephones corrections
    if len(fix) == 18:
        fix = "+34"+fix[:9]+" / +34"+fix[9:]
    if len(fix) == 24:
        fix = fix[:12]+" / "+fix[12:]
    
    return fix


def main():
    file = os.environ['OSMFILE']
    telephone_types = audit(file)
    #pprint.pprint(dict(telephone_types))

    for number in telephone_types:
        better_number = update_telephone(number)
        if (number != better_number):
            print (number, "=>", better_number)
                
if __name__ == '__main__':
    main()