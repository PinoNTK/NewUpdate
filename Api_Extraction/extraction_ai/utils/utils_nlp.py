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
        if c in alphabet+string.printable:
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



s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹỷ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYyy'

def remove_accents(input_str):
	s = ''
	# print(list(u''+input_str))
	for c in list(input_str):
		if c in s1:
			s += s0[s1.index(c)]
		elif c in string.printable+' ':
			s += c


	return s

