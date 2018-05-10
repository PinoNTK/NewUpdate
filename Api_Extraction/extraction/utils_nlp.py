import string
import re
from langdetect import detect_langs
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
cdau = u"àảãáạăằẳẵắặâầẩẫấậèẻẽéẹêềểễếệìỉĩíịòỏõóọôồổỗốộơờởỡớợùủũúụưừửữứựỳỷỹýỵđÀẢÃÁẠĂẰẲẴẮẶÂẦẨẪẤẬÈẺẼÉẸÊỀỂỄẾỆÌỈĨÍỊÒỎÕÓỌÔỒỔỖỐỘƠỜỞỠỚỢÙỦŨÚỤƯỪỬỮỨỰỲỶỸÝỴĐ"
alphabet = string.ascii_letters + string.digits + cdau + "@.+-#&\\/'"  # " ~!@#$%^&*()_+-=[]\;',./{}|:\"<>?"

def clean_string(text):
    text = str(text)
    def lower_first_char(pattern):
        matched_string = pattern.group(0)
        return matched_string[:-1] + matched_string[-1].lower()

    text = re.sub("(?<=[\.\?\)\!\'\"])[\s]*.", lower_first_char, text)

    # Replace weird chars in text

    text = re.sub("’", "'", text)  # special single quote
    text = re.sub("`", "'", text)  # special single quote
    text = re.sub("“", '"', text)  # special double quote
    text = re.sub("？", "?", text)
    text = re.sub("…", " ", text)
    # text = re.sub("é", "e", text)
    res=''
    for c in text:
        if c in alphabet:
            res+=c
        else:
            res+=' '
    # text = ''.join(c for c in text if c in alphabet)
    return ' '.join([t for t in res.split() if len(t.strip())>0])

def match(text):
    return text



def language(text):
    return str(detect_langs(text)[0])[:2]

def classification_language(texts):
    langs = language(str(' '.join(texts)))
    return langs

def preprocessing_text(text):
    text = text.upper()
    text = text.replace(".", " ")
    text = text.replace("/", " ")
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace(":", " ")
    text = text.replace("-", " ")
    text = text.replace(",", " ")
    text = text.replace("<", " ")
    text = text.replace(">", " ")
    text = text.replace("&", " ")
    text = text.replace("[", " ")
    text = text.replace("]", " ")
    text = text.replace("!", " ")
    text = text.strip()
    return text
def clean_title(text):
    res = ''
    for c in text:
        if c in alphabet:
            res += c
        else:
            res += ' '
    # text = ''.join(c for c in text if c in alphabet)
    return ' '.join([t for t in res.split() if len(t.strip()) > 0]).lower()
def get_ngrams(text, n ):
    n_grams = ngrams(word_tokenize(text), n)
    return [ ' '.join(grams) for grams in n_grams]

def format_show(json_cv):
    result={}
    result['language_cv'] = json_cv['language_cv']
    result['image'] = json_cv['image']

    person = json_cv.get('person_details', None)
    result['person_details'] = {}
    if person != None:
        # print('\n---------------------------Personal details--------------------\n')
        for k, v in person.items():
            if k == 'text':
                result['person_details']['descriptions'] = v
            else:
                result['person_details'][k]=v


    education = json_cv.get('education', None)
    result['education'] = {}
    if education != None:
        # print('\n-----------------------------Education---------------------------\n')
        for k, v in education.items():
            if k == 'text':
                result['education']['descriptions'] = v
            else:
                result['education'][k]=v

    skill = json_cv.get('skills', None)
    result['skills'] = {}
    if skill != None:
        # print('\n------------------------Skills------------------------\n')
        for k, v in skill.items():
            if k == 'text':
                result['skills']['descriptions'] = v
            else:
                result['skills'][k]=v

    experiences = json_cv.get('experience', None)
    result['experience'] = []
    if experiences != None:
        # print('\n----------------------------Experience------------------------\n')
        for experience in experiences:
            exp={}
            for k, v in experience.items():
                if k=='text':
                    exp['descriptions']=v
                if k == 'skill' and len(v) > 0:
                    if v.get('programing'):
                        exp['programing'] = v.get('programing')
            result['experience'].append(exp)
    other = json_cv.get('other', None)
    result['other']=[]
    result['objective']=[]
    if other:
        # print('\n-------------------------Other---------------------------\n')
        for k, v in other.items():
            if k=='other':
                result['other'].extend(v)
            elif k=='objective':
                result['objective'].extend(v)
    return result


