from underthesea import word_tokenize
import codecs
import datefinder
import re


title_word = {
    u'CÁC PHÚC LỢI DÀNH CHO BẠN':'PHUC_LOI',
    u'MÔ TẢ CÔNG VIỆC':'MO_TA',
    u'YÊU CẦU CÔNG VIỆC':'YEU_CAU',
    u'CƠ HỘI':'PHUC_LOI',
    u'QUYỀN LỢI':'PHUC_LOI',
    u'CONTACT':'CONTACT',
    u'Quyền lợi được hưởng':'PHUC_LOI',
    u'Thông tin liên hệ':'CONTACT',
    u'Yêu cầu hồ sơ':'HO_SO',
    u'Requirments':'YEU_CAU'
}

title_list = {k.strip().lower():v for k,v in title_word.items()}

def is_title(text):
    if text.isupper():
        return True
    # text += '<a sfs> (ád)'
    text = re.sub(r'\(.*?\)','',text)

    # print(text)
    tokens = text.split()
    tokens = [token for token in tokens if len(token) >0]
    upper = [token for token in tokens if token[0].isupper()]
    if len(tokens)==len(upper):
        return True
    if text.strip().lower() in title_list.keys():
        return True
    return False

if __name__ == '__main__':
    file = codecs.open('Quan_tri_HKT.txt','r','utf-8')
    result = {}
    content=[]
    pre_title = ''
    for line in file:
        if is_title(line):
            if len(content)>0:
                result[pre_title]=content
            content=[]
            pre_title = title_list.get(line.strip().lower(),line)
        else:
            content.append(line)

    if len(content) > 0:
        result[pre_title] = content

    for k,v in result.items():
        print('---------------',k,'-----------------')
        for i in v:
            print(i)