import re
import requests
import json

from django.conf import settings

SPLIT_CHARS = ['|', ' at ', ' through ', ':', ',', '-']

DEFAULT_RULE_BASE_SPLIT_URL = 'http://localhost:8001/api/path/split/?text='

font_style = {
    'italic': ('__ItalicStart__', '__ItalicEnd__'),
    'bold': ('__BoldStart__', '__BoldEnd__'),
    'bolditalic': ('__BoldItalicStart__', '__BoldItalicEnd__'),
    'normal': ('', '')
}

time_keyword = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'now', 'present']
#time_pattern = '\d+\s*-\s*(present|Present|Now|now|Jan|Feb|Mar|Apr|May|June|July|Aug|Sep|Oct|Nov|Dec|\d+)'
time_pattern =  r"(\d+|(Jan|Feb|Mar|Apr|May|June|July|Aug|Sep|Oct|Nov|Dec)\S*)[/\-]?\d+\s*[-?]\s*(\d+|present|Present|Now|now|(Jan|Feb|Mar|Apr|May|June|July|Aug|Sep|Oct|Nov|Dec)\S*)[/\-]?\d+"

def get_fontstyle(part):
    if '__ItalicStart__' in part:
        return 'italic'
    if '__BoldStart__' in part:
        return 'bold'
    if '__BoldItalicStart__' in part:
        return 'bolditalic'
    return 'normal'

def tag_part(part, fs):
    if fs in font_style.keys():
        return font_style[fs][0] + ' ' + part + ' ' + font_style[fs][1]
    else:
        return part 

def split_by_parentheses(line):
    parts = []
    i = 0
    for m in re.finditer('\((.*?)\)', line):
        start = m.start()
        end = m.end()
        if i != start:
            parts.append(line[i:start])
        parts.append(line[start:end])
        i = end
    parts.append(line[i:])
    return parts

def split_by_time(line):
    parts = []
    i = 0
    for m in re.finditer(time_pattern, line):
        start = m.start()
        end = m.end()
        if i != start:
            parts.append(line[i:start])
        parts.append(line[start:end])
        i = end
    parts.append(line[i:])
    return parts    


def split_by_char(line):
    data = []
    result = []
    parts = []
    i = 0
    for m in re.finditer('\((.*?)\)', line):
        start = m.start()
        end = m.end()
        parts.append(line[i:start])
        parts.append(line[start:end])
        i = end
    parts.append(line[i:])
    if parts:
        for part in parts:
            if '(' in part:
                data.append(part[1:-1])
                continue
            is_split = False
            for c in SPLIT_CHARS:
                if c in part:
                    is_split = True
                    if c == '-':
                        m = re.search(time_pattern, part)
                        if m:
                            data.append(part)
                            break
                    part_list = part.split(c)
                    for item in part_list:
                        data += split_by_char(item)
                    break
            if not is_split:
                data.append(part)
    else:
        is_split = False
        for c in SPLIT_CHARS:
            if c in line:
                is_split = True
                if c == '-':
                    m = re.search(time_pattern, line)
                    if m:
                        data.append(line)
                        break
                part_list = line.split(c)
                for item in part_list:
                    data += split_by_char(item)
                break
        if not is_split:
            data.append(line)        
    for item in data:
        if item.strip():
            result.append(item)
    return result

def split_by_font_style(line):
    m = re.finditer('(__ItalicStart__ .*? __ItalicEnd__)|(__BoldStart__ .*? __BoldEnd__)|(__BoldItalicStart__ .*? __BoldItalicEnd__)', line)
    tmp = line
    for item in m:
        text = item.group()
        replace_pattern = ';;;' + text + ';;;'
        tmp = tmp.replace(text, replace_pattern)
    part_list = []
    for item in tmp.split(';;;'):
        if item.strip():
            part_list.append(item)
    return part_list

def old_split_line(line):
    result = []
    for item in split_by_font_style(line):
        fs = get_fontstyle(item)
        if fs != 'normal':
            pattern = font_style[fs][0] + ' (.*?) ' + font_style[fs][1]
            text = re.findall(pattern, item)[0]
        else:
            text = item
        part_list = split_by_char(text)
        for part in part_list:
            #result.append(tag_part(part, fs))
            result.append(part)
    json_list = []
    for item in result:
        data = {'text': item}
        json_list.append(data)
    return json_list

def split_line(line):
    result = []

    for fs_item in split_by_font_style(line):
        fs = get_fontstyle(fs_item)
        if fs != 'normal':
            pattern = font_style[fs][0] + ' (.*?) ' + font_style[fs][1]
            m = re.findall(pattern, fs_item)
            if m:
                text = m[0]
            else:
                text = fs_item
        else:
            text = fs_item

        tmp = []
        for paren_item in split_by_parentheses(text):
            for time_item in split_by_time(paren_item):
                print(time_item)
                for item in split_by_char(time_item):
                    tmp.append(item)
        for i in tmp:
            for item in split_by_rule_base(i):
                result.append(item)
        #for item in split_by_rule_base(text):
        #    result.append(item)
    map_label_key = {
        "O": "other",
        "LOCATION": "location",
        "POSITION": "position",
        "DATE": "time",
        "ORGANIZATION": "company_school"
    }
    json_list = []
    for item in result:
        label = map_label_key.get(item[1])
        if label:
            data = {'text': item[0], "label": label}
            json_list.append(data)
    return json_list

def split_by_rule_base(text):
    result = []
    rule_base_url = getattr(settings, "RULE_BASE_SPLIT_URL", '')
    #rule_base_url = ''
    rule_base_url = rule_base_url if rule_base_url else DEFAULT_RULE_BASE_SPLIT_URL
    re = requests.get(rule_base_url, params={'text': text})
    if re.text:
        a_dict = json.loads(re.text)
        print(a_dict)
        a_list = list(a_dict.get('ORDER'))
        for k in set(a_list):
            count_k = a_list.count(k)
            while count_k > 1:
                a_list.remove(k)
                count_k = a_list.count(k)
        for key in a_dict.get('ORDER'):
            if a_dict.get(key):
                result.append([a_dict.get(key).get('TEXT'), key])
    return result
