import re
import math
import requests
import json

from django.conf import settings
from .company_word_list import company_names
from .career_word_list import career_words
from .stop_word_list import stop_words

time_patterns = [
    r'\d{1,2}[\/\-., \(]?\d{1,2}[\/\-., \)]?\d{2,4}',
    r'\d{0,4}[\/\-., \(]?(\bJan\b|\bFeb\b|\bMar\b|\bApr\b|\bMay\b|\bJun\b|\bJul\b|\bAug\b|\bSep\b|\bOct\b|\bNov\b|\bDec\b|\bSept\b)\S{0,6}[\/\-., \)]?\d{0,4}',
    r'\d{0,4}[\/\-., \(]?(\bJanuary\b|\bFebruary\b|\bMarch\b|\bApril\b|\bMay\b|\bJune\b|\bJuly\b|\bAugust\b|\bSeptember\b|\bOctober\b|\bNovember\b|\bDecember\b)\S{0,6}[\/\-., \)]?\d{0,4}'
]

DEFAULT_STEP = 10

def calculate_level(min_left_margin, max_left_margin, left_margin, height, default_step):
    step = default_step * height / 12 # 12: default font size
    max_step = (max_left_margin - min_left_margin) / step 
    current_step = (left_margin - min_left_margin) / step
    if max_step:
        level = 1 - (current_step / max_step)
    else:
        level = 1
    return level

def percent_font_style(text, full_text):
    fontstyle_map = [("__BoldStart__", "__BoldEnd__"), ("__ItalicStart__", "__ItalicEnd__"), ("__BoldItalicStart__", "__BoldItalicEnd__")]
    full_text_words = full_text.split()
    text_words = text.split()
    if len(text_words) == 0:
        return 0, 0, 0
    result = []
    for fs_map in fontstyle_map:
        start = False
        count = 0
        start_tag = fs_map[0]
        end_tag = fs_map[1]
        for w in full_text_words:
            if w == start_tag:
                start = True
                continue
            if w == end_tag:
                start = False
                continue
            if start:
                count += 1
        percent = count / len(text_words)
        result.append(percent)

    return result

def _percent_company(text):
    text_len = len(text.split())
    if text_len == 0:
        return 0
    count = 0
    for word in text.split():
        if word.upper() in company_names:
            count += 1
    return count / text_len

def _percent_position(text):
    text_len = len(text.split())
    if text_len == 0:
        return 0
    count = 0
    for word in text.split():
        if word.upper() in career_words:
            count += 1
    return count / text_len


def _percent_time(text):
    for pattern in time_patterns:
        m = re.search(pattern, text)
        if m:
            return 1
    return 0


"""
DEFAULT_RULE_BASE_SPLIT_URL = 'http://localhost:8001/api/path/split/?text='
def _percent_time(text):
    result = []
    rule_base_url = getattr(settings, "RULE_BASE_SPLIT_URL", '')
    rule_base_url = rule_base_url if rule_base_url else DEFAULT_RULE_BASE_SPLIT_URL
    re = requests.get(rule_base_url, params={'text': text})
    if re.text:
        a_dict = json.loads(re.text)
        a_list = list(a_dict.get('ORDER'))
        if "DATE" in a_list:
            print(a_list)
            return 1
    return 0
"""

def get_feature_pattern(line, min_left_margin, max_left_margin):
    text = line.get('text')
    full_text = line.get('full_text')
    height = line.get('wh')[1]
    left_margin = line.get('cen')[0]

    bold_percent, italic_percent, bolditalic_percent = percent_font_style(text, full_text)
    font_style_percent = bold_percent + italic_percent + bolditalic_percent
    if font_style_percent > 1:
        font_style_percent = 1

    words = text.split()
    text_length = len(words)
    upper_count = 0
    if text_length > 0:
        for word in words:
            if word.isupper():
                upper_count += 1
    upper_percent = upper_count / text_length
    if font_style_percent < 0.01:
        print("Using upper to detect font style")
        font_style_percent = upper_percent
    
    time_percent = _percent_time(text)
    company_percent = _percent_company(text) * 3
    position_percent = _percent_position(text)
    word_hint_percent = company_percent + position_percent

    level_percent = calculate_level(min_left_margin, max_left_margin, left_margin, height, DEFAULT_STEP)
    return {
        "level": level_percent,
        "word_hint": word_hint_percent,
        "font_style": font_style_percent,
        "time": time_percent,
        "label": ""
    }
    