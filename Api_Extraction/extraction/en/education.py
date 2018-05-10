university_key = ['university']
cpa_key = ['cpa','gpa']

def detect_university(text):
    tokens = text.split()
    for token in tokens:
        if token.lower() in university_key:
            return text
    return None

def detect_cpa(text):
    tokens = text.split()
    for i,token in enumerate(tokens):
        if token.lower() in cpa_key:
            for w in tokens[i+1:]:
                if w.replace('.','',1).isdigit() and float(w)>2 and float(w)<4:
                    return w
    return None