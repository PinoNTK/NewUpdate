from .. import dictionary
import pandas as pd
from os.path import join, dirname ,curdir
import os
import sys
from recruitment_recommender_system.settings import BASE_DIR
sys.path.insert(0, dirname(__file__))

skill = pd.read_excel(join(BASE_DIR,'Api_Extraction/extraction/data/skill_dictionary.xlsx'))

programing = dictionary.Dictionary()
programing.build_dictionary(skill['Programing'])

database = dictionary.Dictionary()
database.build_dictionary(skill['Database'])

framework = dictionary.Dictionary()
framework.build_dictionary(skill['Framework'])

def extract_skill(texts,topics):
    result = {}
    pro = []
    db = []
    fram = []
    description = []
    # result['programing'] = []
    # result['database'] = []
    # result['framework'] = []
    # result['text'] = []
    for text, topic in zip(texts, topics):
        if topic in ['skills', 'experience']:
            pg = detect_programing(text)
            if len(pg) > 0:
                pro.extend(pg)
                # print(result['programing'])

            dt = detect_database(text)
            if len(dt) > 0:
                pro.extend(dt)

            fr = detect_framework(text)
            if len(fr) > 0:
                pro.extend(fr)
        if topic in ['skills']:
            description.append(text)
    if len(pro) > 0:
        result['programing'] = list(set(pro))
    if len(db) > 0:
        result['database'] = list(set(db))
    if len(fram):
        result['framework'] = list(set(fram))
    if len(description) > 0:
        result['text'] = description
    return result


def detect_programing(text):
    result = programing.find(text)
    return result

def detect_database(text):
    result = database.find(text)
    return result

def detect_framework(text):
    result = framework.find(text)
    return result
