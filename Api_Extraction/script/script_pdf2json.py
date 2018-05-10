from Api_Extraction.extraction import Extraction
import json
import glob
import codecs
import datefinder

extraction = Extraction('../../')

def extract_pdf2json(folder):
    for filename in glob.glob(folder+'/*.pdf'):
        if not filename.endswith('.pdf'):
            continue
        result = extraction.parse_cv(filename)
        print(filename)
        outfile = codecs.open(filename[:-4]+'.json','w','utf-8')
        outfile.write(json.dumps(result,ensure_ascii=False))
        outfile.close()
        print(result['person_details'])

def extract_pdf(pathfile):
    result = extraction.parse_cv(pathfile)
    print('Personal Detail')
    for item in result['person_details'].items():
        print(item)
    print('Education')
    for item in result['education'].items():
        print(item)

    print('Skill')
    for item in result['skills'].items():
        print(item)

    print('Experience')
    for item in result['experience']:
        print(item)

    print("Other")
    print(result['other'])
    result = json.dumps(result,ensure_ascii=False)
    return result

def show_cv_json(json_cv):
    person = json_cv.get('person_details',None)
    if person != None:
        print('\n---------------------------Personal details--------------------\n')
        for k,v in person.items():
            if k=='text':
                print('description :')
                for i in v:
                    print('\t',i)
            elif v!= None:
                # if k=='birth_day':
                #     matches = datefinder.find_dates(v)
                #     for match in  matches:
                #         print('birth_day',match.date())
                #
                # else:
                print(k,':',v)

    education = json_cv.get('education',None)
    if education != None:
        print('\n-----------------------------Education---------------------------\n')
        for k, v in education.items():
            if v!= None and len(v)>0 and k!='text':
                print(k,':',v)
            if k=='text' and len(v)>0:
                print('descriptions :')
                for t in v:
                    print('\t',t)

    skill = json_cv.get('skills',None)
    if skill!= None:
        print('\n------------------------Skills------------------------\n')
        for k, v in skill.items():
            if k=='text':
                print('descriptions:')
                for i in v:
                    print('\t',i)
            elif v!= None and len(v)>0 :
                print(k,':',v)

    experiences = json_cv.get('experience',None)
    if experiences!= None:
        print('\n----------------------------Experience------------------------\n')
        for experience in experiences:
            for k,v in experience.items():
                if v!= None and len(v)>0 and k!='skill':
                    print(k,':',v)
                if k=='skill' and len(v)>0:
                    if v.get('programing'):
                        print('programing',v['programing'])


    other = json_cv.get('other',None)
    if other:
        print('\n-------------------------Other---------------------------\n')
        for k,v in other.items():
            print('**',k)
            for i in v:
                print('\t',i)
def format_show(json_cv):
    result={}
    result['language_cv'] = json_cv.get('language_cv',None)
    result['image'] = json_cv['image']

    person = json_cv.get('person_details', None)
    result['person_details'] = {}
    if person != None:
        print('\n---------------------------Personal details--------------------\n')
        for k, v in person.items():
            if k == 'text':
                result['person_details']['descriptions'] = v
            else:
                result['person_details'][k]=v


    education = json_cv.get('education', None)
    result['education'] = {}
    if education != None:
        print('\n-----------------------------Education---------------------------\n')
        for k, v in education.items():
            if k == 'text':
                result['education']['descriptions'] = v
            else:
                result['education'][k]=v

    skill = json_cv.get('skills', None)
    result['skills'] = {}
    if skill != None:
        print('\n------------------------Skills------------------------\n')
        for k, v in skill.items():
            if k == 'text':
                result['skills']['descriptions'] = v
            else:
                result['skills'][k]=v

    experiences = json_cv.get('experience', None)
    result['experience'] = []
    if experiences != None:
        print('\n----------------------------Experience------------------------\n')
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
        print('\n-------------------------Other---------------------------\n')
        for k, v in other.items():
            if k=='other':
                result['other'].extend(v)
            elif k=='objective':
                result['objective'].extend(v)
    return result

if __name__ == "__main__":
    extraction = Extraction('../../')
    # extract_pdf2json('../../../../Machine Learning/ReadPDF/data/cv/en/done')
    # result = extraction.parse_cv('../../../../Machine Learning/ReadPDF/data/cv/en/done/ITSOL_CV_IOS_LEPHUONG.pdf')
    # result = extraction.parse_cv('../../../../Machine Learning/ReadPDF/data/cv/vi/HR - Vu-Thi-Thu.pdf')
    # show_cv_json(result)
    # show_cv_json(extraction.parse_cv('../../../../Machine Learning/ReadPDF/data/cv/en/done/ITSOL_CV_IOS_ Ta Cuong.pdf'))
    # extract_pdf('../../../../Machine Learning/ReadPDF/data/cv/en/done/ITSOL_CV_IOS_ Ta Cuong.pdf')
    # extract_pdf('../../../../Machine Learning/ReadPDF/data/cv/vi/HR - Vu-Thi-Thu.pdf')
    # extract_pdf('../cv/pham_van_tien.docx')
    folder = 'D:\Documents\ITSOL\data\pdf\en'
    i=0
    for filename in glob.glob(folder + '/*.pdf'):
        print(filename)
        result =extraction.parse_cv(filename)
        if len(result)==0:
            continue
        # result = format_show(result)
        with codecs.open(filename[:-4]+'.json','w','utf-8') as output:
            output.write(json.dumps(result,ensure_ascii=False))
        if i>1:
            break
        i+=0
        # show_cv_json(result)