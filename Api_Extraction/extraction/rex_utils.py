import re
from unidecode import unidecode


def text_format_space(text: str) -> str:
    text = unidecode(text)
    text = re.sub(r'\*', ' ', text)
    text = re.sub(r'•', ' ', text)
    text = re.sub(r'', ' ', text)
    text = re.sub(r'▪', ' ', text)
    text = re.sub(r'-', ' ', text)
    text = re.sub(r'‐', '-', text)
    text = re.sub(r':-', ': ', text)
    text = re.sub(r'：', ': ', text)
    text = re.sub(r'—', ' ', text)
    text = re.sub(r'_', ' ', text)
    text = re.sub(r'\)', ') ', text)
    text = re.sub(r';', ' ', text)
    text = re.sub(r',', ', ', text)
    text = re.sub(r'\:', ': ', text)
    text = re.sub(r' \:', ': ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def text_format(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'–', '-', text)
    text = re.sub(r' – ', '-', text)
    text = re.sub(r'– ', '-', text)
    text = re.sub(r' –', '-', text)
    text = re.sub(r' - ', '-', text)
    text = re.sub(r' -', '-', text)
    text = re.sub(r'- ', '-', text)
    text = re.sub(r' \/ ', '/', text)
    text = re.sub(r' \/', '/', text)
    text = re.sub(r'\/ ', '/', text)
    text = re.sub(r' : ', ': ', text)
    text = re.sub(r' :', ': ', text)
    text = re.sub(r' ,', ',', text)
    return text


def remove_keyword(text: str) -> str:
    keywords = [
        'manager', 'designer', 'developer'
    ]
    regex = r'(' + '|'.join(keywords) + ')'
    text = re.sub(regex, ' ', text, 0, re.IGNORECASE)
    return text


# detect phone label
def detect_phone_label(text: str) -> str:
    patterns = [
        "mobile phone number(|\d)",
        "mobile phone(|\d)",
        "mobile number(|\d)",
        "mobile(|\d)",
        "(mobile)(|\d)",
        "phone number(|\d)",
        "phone(|\d)",
        "phone(|\d)#",
        "telephone(|\d)",
        "telephone number(|\d)",
        "tel(|\d)",
        "call me(|\d)",
        "contact(|\d)",
        "contact no(|\d)",
    ]
    pattern = r'(' + '|'.join(patterns) + ')( :|:| : )'
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None


# detect phone
def detect_phone(text: str, prefix) -> str:
    if prefix != None:
        prefix = '(' + prefix + '( |))'
    else:
        prefix = ''
    patterns = [
        '(' + prefix + '(\+|-:|\s)(\d{1,3})([ .-])(\d{1,3})([ .-])(\d{2,4})([ .-])(\d{2,4}))',
        # 81 080 4250 5700/81-080-4250-5700/+81 080 4250 5700/+81-080-4250-5700/81.080.4250.5700/+81.080.4250.5700
        '(' + prefix + '(\((\+|)\d{1,}\)|(\+|)\d{1,})([ .-])(\d{8,}))',
        # (65) 91593143|(+65) 91593143 / (+6243)-91593143 / (+6243).91593143 / +61-8033593768 / +61 8033593768 /  +61.8033593768
        '(' + prefix + '(\((\+|)\d{1,}\)|(\+|)\d{1,})([ .-])(\d{1,})([ .-])(\d{4,}))',
        # +61-4-22023139 /  +61.4.22023139 / +61 4 22023139 / 080-4250-5700 / 080 4250 5700 / 080.4250.5700
        '(' + prefix + '(\((\+|)\d{1,}\))([ .-])(\d{1,})([ .-])(\d{3,})([ .-])(\d{3,}))',
        # (+1) 206-319-8637 / (1) 206-319-8637
        '(' + prefix + '((\+|)\d{1,})([ .-])(\(\d{1,}\))([ .-|]\d{1,})([ .-])(\d{3,})([ .-])(\d{3,}))',
        # +81 (0)90-8005-1144 / 81 (0)90-8005-1144
        '(' + prefix + '(\+|)(\d{1,3})([ /|])(\(\d{1,}\))([ .-|])(\d{8,}))',
        # +81/(1)8033938585 / +33 (0)557248612
        '(' + prefix + '(\+|)(\d{1,3})(\(\d{1,}\))([ .-|])(\d{8,}))',
        # +81(1)8033938585 / 33(0)557248612
        '(' + prefix + '(\+|)(\((\d+)([ ,-])(\d+)([ ,-])(\d+)\)))',
        # +(90-8005-1144) / (90-8005-1144)
        '(' + prefix + '((\+|)\d{1,}\d{9,}))',
        # +9080051144) / 9080051144
        '(' + prefix + '(\([0-9]{1,3}\))([ .-|])(\d{2,4})([ .-])(\d{2,4}))',
        # (080) 4613-8686 / (080)4613-8686 / (080) 4613 8686 / (080)4613 8686
        '(' + prefix + '(\(\+\d{1,}\))(\s)([0-9 ]+))',
        # (+33) 6 99 19 59 88
    ]
    pattern = r'|'.join(patterns)
    matches = re.finditer(pattern, text, re.IGNORECASE)
    for matchNum, match in enumerate(matches):
        return match.group()
    return None


def detect_email_label(text: str) -> str:
    patterns = [
        " e mail address(|\d)",
        "email address(|\d)",
        "email id(|\d)",
        " e mail(|\d)",
        "mail address(|\d)",
        "mail(|\d)",
        "e-mail address(|\d)",
        "e-mail(|\d)",
    ]
    regex = r'(' + '|'.join(patterns) + ')( :|:| : | )'
    match = re.search(regex, text, re.IGNORECASE)
    if match:
        return match.group()
    else:
        return None


def detect_email(text: str, prefix) -> str:
    if prefix != None:
        prefix = '(' + prefix + '( |))'
    else:
        prefix = ''
    patterns = [
        '((' + prefix + '[\w.-_]+@[\w.-_]+)([/|\|])(' + prefix + '[\w.-_]+@[\w.-_]+))',
        '(' + prefix + '[\w.-_]+@[\w.-_]+)',
    ]
    pattern = r'|'.join(patterns)
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None


def detect_fax(text: str, prefix) -> str:
    if prefix != None:
        prefix = '(' + prefix + '( |))'
    else:
        prefix = ''
    patterns = [
        '(' + prefix + '([0-9]{1,3})[ .-][0-9]{3,4}[ .-][0-9]{4})',
        '(' + prefix + '\([0-9]{1,3}\)[ .-][0-9]{3,4}[ .-][0-9]{4})',
        '(' + prefix + '(\([0-9]{1,3}\))[0-9]{1,3}([0-9]{1,3})[ .-][0-9]{3,4}[ .-][0-9]{4})',
        '(' + prefix + '([0-9]{1,3})[ .-](\([0-9]{1,3}\))[0-9]{1,3}([0-9]{1,3})[ .-][0-9]{3,4}[ .-][0-9]{4})',
        '(' + prefix + '([0-9]{1,3})[ .-][0-9]{1,3}([0-9]{1,3})[ .-][0-9]{3,4}[ .-][0-9]{4})',
    ]
    pattern = r'|'.join(patterns)

    matches = re.finditer(pattern, text, re.IGNORECASE + re.MULTILINE)

    for matchNum, match in enumerate(matches):
        return re.sub(r'\s+', " ", match.group())
    return None


def detect_fax_label(text: str) -> str:
    patterns = [
        "fax(|\d)",
    ]
    pattern = r'(' + '|'.join(patterns) + ')( :|:| : | )'
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None


def detect_nationality(text: str, prefix) -> str:
    if prefix != None:
        prefix = '(' + prefix + '( |))'
    else:
        prefix = ''
    patterns = [
        '(' + prefix + '([\w|\s])([a-z]{1,}))',
    ]
    pattern = r'|'.join(patterns)
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None


def detect_nationality_label(text: str) -> str:
    patterns = [
        "nationality(|\d)",
        "country(|\d)",
        "place of birth(|\d)",
        "d.o.b(|\d)",
        "place of residence(|\d)",
    ]
    # pattern = r'('+'|'.join(patterns)+')( :|:| : | )'
    # match = re.search(pattern, text, re.IGNORECASE)

    for patten in patterns:
        regex = r'(' + patten + ')( :|:| : | )'
        matches = re.search(regex, text, re.IGNORECASE)
        if matches:
            return matches.group()

    return None


def detect_facebook_label(text: str) -> str:
    patterns = [
        "facebook(|\d)",
        "fb(|\d)",
    ]
    pattern = r'(' + '|'.join(patterns) + ')( :|:| : | )'
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None


def detect_facebook(text: str, prefix) -> str:
    if prefix != None:
        prefix = '(' + prefix + '( |))'
    else:
        prefix = ''
    patterns = [
        '(' + prefix + '(?:https?:\/\/)?(?:www\.)?(mbasic.facebook|m\.facebook|facebook|fb)\.(com|me)\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*))',
    ]
    pattern = r'|'.join(patterns)
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None


def detect_linkedin_label(text: str) -> str:
    patterns = [
        "linkedin(|\d)",
    ]
    pattern = r'(' + '|'.join(patterns) + ')( :|:| : | )'
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None


def detect_linkedin(text: str, prefix) -> str:
    if prefix != None:
        prefix = '(' + prefix + '( |))'
    else:
        prefix = ''
    patterns = [
        '(' + prefix + '(((http|https):\/\/?)?((www|\w\w)\.)?linkedin.com(\w+:{0,1}\w*@)?(\S+)(:([0-9])+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?))',
    ]
    pattern = r'|'.join(patterns)
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None


def detect_twitter_label(text: str) -> str:
    patterns = [
        "twitter(|\d)",
        "t(|\d)",
    ]
    pattern = r'(' + '|'.join(patterns) + ')( :|:| : | )'
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None


def detect_twitter(text: str, prefix) -> str:
    if prefix != None:
        prefix = '(' + prefix + '( |))'
    else:
        prefix = ''
    patterns = [
        '(' + prefix + '((?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:#!\/)?@?([^\/\?\s]*)))',
    ]
    pattern = r'|'.join(patterns)
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None


# Birth date
def detect_birthdate_label(text: str) -> str:
    patterns = [
        "birthdate(|\d)",
        "birth date(|\d)",
        "birthday(|\d)",
        "birth day(|\d)",
        "birth(|\d)",
        "date of birth(|\d)",
    ]
    pattern = r'(' + '|'.join(patterns) + ')( :|:| : | )'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group()
    else:
        return None


def detect_birthdate(text: str, prefix) -> str:
    if prefix != None:
        prefix = '(' + prefix + '( |))'
    else:
        prefix = ''
    signs = '(( / |/| /|/ )|(| )|( - |-| -|- )|( . |.| .|. )|( , |,| ,|, )|(| ))'
    patterns = [
        '(' + prefix + '((\d){2,4}' + signs + '(\d){1,2}' + signs + '(\d){1,2}))',
        '(' + prefix + '((\d){1,2}' + signs + '(\d){1,2}' + signs + '(\d){2,4}))',
        '(' + prefix + '([a-z]{3}' + signs + '(\d+)' + signs + '(\d+)))',
        '(' + prefix + '([a-z]{3}' + signs + '([a-z]{3})' + signs + '(\d+)))',
        #'(' + prefix + '([a-z]{3}' + signs + '(\d+)' + signs + '([a-z]{3})))',
        #'(' + prefix + '(\([a-z]{3}' + signs + '(\d+)' + signs + '(\d+)\)))',
        #'(' + prefix + '((\d){1,2}' + signs + '[a-z0-9]{3,7}' + signs + '(\d){1,4}))',
        #'(' + prefix + '([a-z0-9]{1,4}' + signs + '[a-z0-9]{3,8}' + signs + '(\d){4}))',
    ]
    pattern = r'|'.join(patterns)
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group()
    else:
        return None


def detect_url(text: str) -> str:
    matches = re.finditer(
        r"(http://|https://|www.|http://www.|https://www.)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        text, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        text = text.replace(match.group(), '')

    return text


def detect_address(text: str, prefix) -> str:
    countries = 'Japan|China|France|Singapore|Philippines|Korea|Australia|Vietnam|Thailand|Italy|Germany|India|Canada|Malaysia|Netherlands|Spain|Taiwan|Indonesia|Hong Kong'
    specials = "#\d+|a-z:.,àâæéêèëïîôœûùç_'’-"
    zipcode = 'AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY|KL'
    regexs = [
        '(\d{2,4})(,)? ([a-z0-9#|.,]{1,}\s){3,9}(' + zipcode + ')([,:]{0,1} [0-9]{5}(-[0-9]{4})?)',
        # 2205 Bridgepointe Pkwy San Mateo, CA 94404
        '(\d{2,4})(,)? ([a-z0-9#|.,]{1,}\s){3,9}(' + zipcode + ')\s',
        # 2205 Bridgepointe Pkwy San Mateo, CA
        '(\d{1,4}) (([' + specials + ']){1,}\s){2,9}(' + countries + ')([,:]{0,1} [0-9]{5,}(-[0-9]{4})?)',
        # 182 Bukit Batok West Avenue 8 #09-141, Singapore 650182 / 182 Bukit Batok West Avenue 8 #09-141, Singapore 650182-312
        '(\d{1,4}) (([' + specials + ']){1,}\s){2,9}(' + countries + ')',
        # 1 allée de l’hospitalité Appt : D3 Villeneuve d’Ascq, France
        # '(' + prefix + '(([\d-]{1,3}){2,}\s[a-z-,]{2,30}\s[a-z-,]{2,15}\s[a-z-,]{2,15}\s[a-z-,]{2,15}\s[0-9-,]{2,15}))',
        # '(' + prefix + '((([0-9]{1,4}?-){1,3}\d{1,4}){1}[,]([a-z-, ]{2,30}){3,}[:](\d{2,3}-\d{3,5})))',
        # '(' + prefix + '(\d{2,}(\s{1}([#\d+|a-z-.,]){1,}){2,}\s{1}?([a-z]{2,}[-][0-9]{3,6})))',
        # '(' + prefix + '(\d{2,}(\s{1}([#\d+|a-z-.,]){1,}){2,}(\s{1}?\w{1,})(\d){3,6}))',
        # '(' + prefix + '(\d{2,}(\s{1}([#\d+|a-z-.,]){1,}){2,}(\s{1}?\w{1,})))',
        # '(' + prefix + '(\d+) ((\w+[ ,])+ ){2}([a-zA-Z]){2} (\d){5})',
    ]
    if prefix != None:
        prefix = '(' + prefix + '( |))'
        regexs_label = [
            '(' + prefix + '([\s\w,.\-_0-9]+) (' + countries + '))',
            # Male Place of Residence: Kajigaya, Sakae ku, Yokohama City, Kanagawa Prefectural, Japan
        ]
        regexs.extend(regexs_label)
    regex = r'|'.join(regexs)
    matches = re.finditer(regex, text, re.IGNORECASE)
    for matchNum, match in enumerate(matches):
        return match.group()
    # for patten in regexs:
    #     regex = r'' + patten
    #     matches = re.search(regex, text, re.IGNORECASE)
    #     if matches:
    #         return matches.group()

    return None


def detect_address_label(text: str) -> str:
    patterns = [
        "address(|\d)",
        "resides(|\d)",
        "current location(|\d)",
        "place of work(|\d)",
        "home contact information(|\d)",
    ]
    pattern = r'(' + '|'.join(patterns) + ')( :|:| : | )'
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None

def detect_address_sub(text: str) -> str:
        countries = 'Japan|China|France|Singapore|Philippines|Korea|Australia|Vietnam|Thailand|Italy|Germany|India|Canada|Malaysia|Netherlands|Spain|Taiwan|Indonesia|Hong Kong'
        cities = 'Tokyo|Osaka|Francisco|Mateo|Chiba|California|Setagaya|New York|Melbourne|Vic|Ozenji'
        regexs = [
            '([\s\w,.\-_0-9]+) (' + countries + ')',
            '([\s\w,.\-_0-9]+) (' + cities + ')([,:]{0,1} [0-9]{5}(-[0-9]{4})?)',
            '([\s\w,.\-_0-9]+) (' + cities + ')',

        ]
        regex = r'|'.join(regexs)
        matches = re.finditer(regex, text, re.IGNORECASE)
        for matchNum, match in enumerate(matches):
            return match.group()
        return None

# Languages
def detect_language_label(text: str) -> str:
    patterns = [
        "languages(|\d)",
        "language(|\d)",
        "languages spoken(|\d)",
        "language ability(|\d)",
    ]
    pattern = r'(' + '|'.join(patterns) + ')( :|:| : | )'
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None


def detect_language(text: str, prefix) -> str:
    if prefix != None:
        prefix = '(' + prefix + '( |))'
    else:
        prefix = ''
    signs = '(( [–|-] |[–|-]| [–|-]|[–|-])|( / |/| /|/ )|(| ))'
    patterns = [
        '(' + prefix + '(([a-z]{3,})' + signs + '([a-z]{3,}))(, | , | ,|)(([a-z]{3,})' + signs + '([a-z]{3,})))',
        '(' + prefix + '(([a-z]{3,})' + signs + '([a-z]{3,})))',
    ]
    pattern = r'|'.join(patterns)
    match = re.search(pattern, text, re.IGNORECASE + re.MULTILINE)
    if match:
        return match.group()
    else:
        return None
