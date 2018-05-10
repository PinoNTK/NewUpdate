import re

class DateTime(object):
    def __init__(self):
        self.month = {
            'january':1,
            'jan':1,
            'february':2,
            'feb':2,
            'march':3,
            'mar':3,
            'april':4,
            'apr':4,
            'may':5,
            'june':6,
            'jun':6,
            'july':7,
            'jul':7,
            'august':8,
            'aug':8,
            'september':9,
            'sep':9,
            'october':10,
            'oct':10,
            'november':11,
            'nov':11,
            'december':12,
            'dec':12
        }
    def get_date(self,s):
        s=s.strip().lower()
        s = ' '.join([x for x in s.split() if len(x) > 0])
        s=s.replace('\\','/')
        s=s.replace('-','/')
        s=s.replace('.','/')
        s = s.replace('/ ', '/')
        s = s.replace(' /', '/')
        s=s.split()
        s=[x for x in s if len(x)>0]
        if len(s)==1:
            date=s[0].split('/')
            if len(date)==0:
                return None
            elif len(date)==1:
                if len(date[0])==4:
                    return 1,1,date[0]
            elif len(date)==2:
                return 1,date[0],date[1]
            d,m,y = date
            return d,m,y
        elif len(s)==2:
            return 1,self.month.get(s[0],s[0]),s[1]
        else:
            return s[0],self.month.get(s[1],s[1]),s[2]

    def has_date(self,text):
        # print(text)
        text =text.strip().lower()
        if len(text)<5:
            return 0
        s = text
        s = ' '.join([x for x in s.split() if len(x) > 0])

        s = s.replace('\\', '/')
        s = s.replace('-', '/')
        s = s.replace('.', '/')
        s = s.replace('/ ', '/')
        s = s.replace(' /', '/')
        max_len = 1
        for m in self.month.keys():
            if text.find(m)>-1:
                if len(m)>max_len:
                    max_len=len(m)
        patterns = ['\d{4}/\d{1,2}/\d{1,2}','\d{1,2}/\d{1,2}/\d{4}','\d{1,2}/\d{4}']
        for pattern in patterns:
            if len(re.findall(pattern,s))==1:
                if len(pattern)-6>max_len:
                    max_len = len(pattern)-6
        return max_len

rex_time = DateTime()