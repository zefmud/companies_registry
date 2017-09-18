import sys
import csv
from xml.parsers import expat
import codecs
import pandas as pd
from csv import writer

OUTPUT_FILE = "companies_founders.csv"
XML_FILE = '15.1-EX_XML_EDR_UO.xml'

fields = ['NAME', 'SHORT_NAME', 'EDRPOU', 'ADDRESS', 'BOSS', 'KVED', 'STAN', "FOUNDER"]


def dump_company():
    global company
    for c in company:
        if company[c] == []:
            company[c] = ['']
    df = pd.DataFrame(company['FOUNDER'])
    for c in company:
        if c != 'FOUNDER':
            df[c] = company[c][0]
    df = df[fields]
    df.to_csv(OUTPUT_FILE, mode = 'a', header = False, index = False)

def start_element(name, attrs):
    global company, content, isData
    if name in fields:
        isData = True
    else:
        isData = False

def company2nulls():
    global company
    company = {}
    for f in fields:
        company[f] = []

def end_element(name):
    global company, content
    if name == "RECORD":
        dump_company()
        company2nulls()
    elif name in fields:
        company[name].append(content)
    content = ''

def char_data(data):
    global content
    if isData:
        content += data


if __name__ == "__main__":
    p = expat.ParserCreate()
    company2nulls()
    content = ''
    isData = False
    with open(OUTPUT_FILE, 'w') as of:
        of_writer = writer(of)
        of_writer.writerow(fields)
    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data
    with codecs.open(XML_FILE, 'r', 'cp1251') as f:
        file_content = f.read()
        p.Parse(file_content)
