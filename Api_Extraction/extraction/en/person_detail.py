import re
from .. import rex_utils as rex
from ..utils_time import rex_time
from .title_word_list import profile_words
from .. import utils_nlp
name_begin = ['name','name:']
name_end = ['nationality','birth','day','date','male','job','telephone','candidate','address','gender','birth day','birth']
birth_begin = ['birth day','birth','day','date']
sex_begin = ['sex','gender']
sex_key = ['male','female','men']
phone_key = ['number','phone']
email_key = ['mail']
address_key = ['address','nationality']
address_end = ['.','gender','mobile','mail','date','day','birth']


def extract_detail(texts,topics):
    result = {}
    result['name'] = u'Họ tên'
    result['birth_day'] = u'Ngày sinh'
    result['sex'] = u'Giới tính'
    result['address'] = u'Địa chỉ'
    result['mail'] = u'Mail'
    result['number'] = u'Số điện thoại'
    result['text'] = []
    for text,topic in zip(texts,topics):
        if topic == 'personal_details':

            name = detect_name(text)
            if name != None:
                result['name'] = name
            birth_day = detect_year(text)
            if birth_day != None:
                result['birth_day'] = birth_day
            sex  = detect_sex(text)
            if sex != None:
                result['sex'] = sex
            address = rex.detect_address(text,'')
            if address!= None:
                result['address']=address
            mail = detect_mail(text)
            if mail != None:
                result['mail'] = mail
            number = detect_number(text)
            if number != None:
                result['number'] = number
            result['text'].append(text)
    return result




def detect_name(text):
    flag = False
    # print(text)
    text = utils_nlp.preprocessing_text(text)
    text = text.split()
    for i,token in enumerate(text):
        if token.lower() in name_begin:
            flag = True
            name = ''
            for w in text[i+1:]:
                if w[0].isupper() and w.lower() not in name_end:
                    name+= ' '+w
                else:
                    return name.strip()
            return name.strip()
    return None

def detect_year(text):
    text = text.split()
    for i, token in enumerate(text):
        if token.lower() in birth_begin:
            for w in text[i + 1:]:
                if len(w)==4 and w[0]=='1' and w.isdigit():
                    return w
    return None

def detect_sex(text):
    text = text.split()
    for i, token in enumerate(text):
        if token.lower() in sex_begin:
            for sex in text[i + 1:]:
                if sex.lower() in sex_key:
                    return sex
    return None

def detect_address(text):
    flag = False
    text = text.split()
    for i, token in enumerate(text):
        if token.lower() in address_key:
            flag = True
            address = ''
            for w in text[i + 1:]:
                if w[-1] != '.' and w.lower() not in address_end:
                    address += ' ' + w
                else:
                    return address
            return address
    return None

def detect_number(text):
    number = re.findall(r"[0-9. ]{10,16}",text)
    if len(number)>0:
        return number[0]
    return None

def detect_mail(text):
     mail = re.findall(r"([a-zA-Z0-9][a-zA-Z0-9_.+-]*@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)",text)
     if len(mail)>0:
         return mail[0]
     return None