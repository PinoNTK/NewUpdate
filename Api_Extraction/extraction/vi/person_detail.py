import re
from underthesea import word_tokenize
from .. import utils_nlp
name_begin = [u'tên',u'tên:',u'họ tên',u'họ và tên']
name_end = [u'quốc tịch',u'ngày sinh',u'địa chỉ',u'giới tính','ngày','job','telephone','candidate','address']
birth_begin = ['birth day','birth','day','date']
sex_begin = [u'giới', u'tính']
sex_key = [u'nam',u'nữ']
phone_key = ['number','phone']
email_key = ['mail']
address_key = [u'địa chỉ',u'hộ khẩu',u'nơi ở']
address_end = ['.',u'website',u'giới tính',u'địa chỉ']


def detect_nameX(text):
    text = utils_nlp.clean_string(text)
    text = word_tokenize(text)
    # print(text)
    for i,token in enumerate(text):
        if token in name_begin:
            name = ''
            for w in text[i+1:]:
                if w[0].isupper() and w not in name_end:
                    name+=w+' '
                elif len(name)>5:
                    return name.strip()
            if len(name.strip())>5:
                return name.strip()
    return None

def detect_name(text):
    # print(text)
    flag = False
    # text = utils_nlp.preprocessing_text(text)
    ngram_1 = utils_nlp.get_ngrams(text,1)
    if len(ngram_1)<2:
        return None
    ngram_2 = utils_nlp.get_ngrams(text,2)
    ngram_2.append(ngram_1[-1])
    text = list(zip(ngram_1,ngram_2))
    for i,token in enumerate(text):
        token,_=token
        # print(token)
        if token.lower() in name_begin:
            flag = True
            name = ''
            for w,w2 in text[i+1:]:
                # w,w2 = w
                if w[0].isupper() and w2.lower() not in name_end and w.lower() not in name_end:
                    name+= ' '+w
                elif len(name.strip())>5:
                    # print(name)
                    return name.strip()
            # print(name)
            if len(name.strip())>5:
                return name.strip()
    return None

def detect_year(text):
    text = text.split()
    for i, token in enumerate(text):
        if token.lower() in birth_begin:
            flag = True
            name = ''
            for w in text[i + 1:]:
                if len(w)==4 and w[0]=='1' and w.isdigit():
                    return w
    return None

def detect_sex(text):
    text = text.split()
    for i, token in enumerate(text):
        if token.lower() in sex_begin:
            for sex in text[i+1:]:
                if sex.lower() in sex_key:
                    if sex in ['nam']:
                        return 'Male'
                    else:
                        return 'Female'
                    return sex
    return None

def detect_address(text):
    flag = False
    ngram_1 = utils_nlp.get_ngrams(text, 1)
    if len(ngram_1) < 2:
        return None
    ngram_2 = utils_nlp.get_ngrams(text, 2)
    ngram_2.append(ngram_1[-1])
    text = list(zip(ngram_1, ngram_2))
    before = u''
    for i, token in enumerate(text):
        token,_=token
        if before+' '+ token.lower() in address_key:
            flag = True
            address = ''
            for w,w2 in text[i + 1:]:
                if w[-1] != '.' and w2.lower() not in address_end and w.lower() not in address_end:
                    address += ' ' + w
                else:
                    return address
            return address
        before = token.lower()
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