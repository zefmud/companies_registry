import sys
import csv
from xml.parsers import expat
import codecs
import pandas as pd
from csv import writer

OUTPUT_FILE = "companies_founders.csv"


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
        #print(content)
        company[name].append(content)
    content = ''


def char_data(data):
    global content
    #print(isData, data)
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
    with codecs.open("/home/pavlo/texty.org.ua/registry/15.1-EX_XML_EDR_UO.xml", 'r', 'cp1251') as f:
        file_content = f.read()
        p.Parse(file_content)
