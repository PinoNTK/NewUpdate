from .utils.pdf_utils import PdfReader,PDFObject
from .utils import utils_file,utils_nlp
import os
import codecs
import json
import glob
import shutil
import numpy as np
import pandas as pd

pdfreader = PdfReader('temp')
def pdf2json(path):
    if path.endswith('pdf'):
        # path = os.path.join(root, filename)
        # txtout = os.path.join(dir_output, filename[:-3] + 'txt')
        # jsonout = os.path.join(dir_output, filename[:-3] + 'json')
        # ann = os.path.join(dir_output, filename[:-3] + 'ann')
        _, clusters, objs, images = pdfreader.parse(path, 1, False)

        # with codecs.open(txtout, 'w', 'utf-8') as writer, codecs.open(jsonout, 'w', 'utf-8') as jsonwriter:
        #     codecs.open(ann, 'w', 'utf-8')
        text = ''
        dict_objs = []
        for obj in objs:
            if obj.type == 'TextRect':
                for c in obj.childrens:
                    dict_objs.append(c.to_dict())
                    text += c.text+'\n'
                    # writer.write(c.text + '\n')
            else:
                dict_objs.append(obj.to_dict())
                text += obj.text + '\n'
                # writer.write(obj.text + '\n')
        # objs = [obj.__dict__ for obj in objs]
        # json_cv = json.dumps(dict_objs, ensure_ascii=False)
        return dict_objs,text,images
    return {}
def pdf2tokens(path,output=None):
    json_data,text_data,images = pdf2json(path)
    idx = 0
    # print(json_data)
    for obj in json_data:
        # print(obj)
        if len(obj['text'].strip()) > 0:
            start = text_data.index(obj['text'].strip(), idx)
            if start >= 0:
                obj['start'] = start
                obj['end'] = start + len(obj['text'].strip())
                idx = obj['end']

    tokens = []
    for obj in json_data:
        tks = split_token(obj['text'], obj['start'])
        for token in tks:
            token['obj'] = obj
            tokens.append(token)
    return tokens,images

def pdf_folder_to_json(dir_cv,dir_output):
    utils_file.create_folder(dir_output)
    for root, dir, files in os.walk(dir_cv):
        for filename in files:
            if filename.endswith('pdf'):
                path = os.path.join(root, filename)
                txtout = os.path.join(dir_output,filename[:-3]+'txt')
                jsonout = os.path.join(dir_output,filename[:-3]+'json')
                ann = os.path.join(dir_output, filename[:-3] + 'ann')
                _, clusters,objs, _ = pdfreader.parse(path, 1, False)

                with codecs.open(txtout,'w','utf-8') as writer , codecs.open(jsonout,'w','utf-8') as jsonwriter:
                    codecs.open(ann, 'w', 'utf-8')

                    dict_objs = []
                    for obj in objs:
                        if obj.type == 'TextRect':
                            for c in obj.childrens:
                                dict_objs.append(c.to_dict())
                                writer.write(c.text + '\n')
                        else:
                            dict_objs.append(obj.to_dict())
                            writer.write(obj.text + '\n')
                    # objs = [obj.__dict__ for obj in objs]
                    json.dump(dict_objs, jsonwriter,ensure_ascii=False)


def cluster_cv(dir):
    # os.path.dirname()
    for root, dir, files in os.walk(dir):
        for filename in files:
            if filename.endswith('pdf'):
                print(filename)
                texts, _, _, _ = pdfreader.parse(os.path.join(root, filename))
                lang = utils_nlp.classification_language(texts)
                if not os.path.exists(os.path.join(root,lang)):
                    os.makedirs(os.path.join(root,lang))
                shutil.move(os.path.join(root,filename),os.path.join(root,lang,filename))
        break
def split_token(text,start=0):
    tokens = []
    token = {}
    token['start'] = 0
    for i, ch in enumerate(text):
        if ch == '\n' or ch == ' ':
            token['end'] = i
            if i > token['start']:
                token['text'] = text[token['start']:token['end']]
                token['start'] +=start
                token['end']+=start
                tokens.append(token)
            token = {}
            token['start'] = i + 1

        split_ch = "()!-+:;',"
        split_ch1 = "@/.()!-+:;',"
        if ch in list(split_ch):
            token['end'] = i
            if i > token['start']:
                token['text'] = text[token['start']:token['end']]
                token['start'] +=start
                token['end']+=start
                tokens.append(token)

            token={}
            token['start']=i+start
            token['text']=ch
            token['end'] = i+start+1
            tokens.append(token)

            token = {}
            token['start'] = i + 1


    if len(text) > token['start']:
        token['text'] = text[token['start']:].strip()
        token['end'] = token['start'] + len(token['text'])
        token['start'] += start
        token['end'] += start
        tokens.append(token)
    return tokens

def get_entities(text,entity_data,type='entity'):
    entities=[]
    for line in entity_data:
        if len(line.strip())>0 and line[0]=='T':
            entity={}
            line=line.split()
            entity['id']=line[0]
            entity['label']=line[1]
            if type == 'entity':
                if line[1].endswith('Content'):
                    continue
            elif type == 'content':
                if not (line[1].endswith('Content') or line[1].endswith('Title')):
                    continue
            entity['start']=int(line[2])
            end = 3
            while not line[end].isdigit():
                end+=1
            entity['end'] = int(line[end])
            entity['text'] = ' '.join(line[end+1:])
            entities.append(entity)
    return entities

def merge_token_with_entity(tokens,entities):
    entities = sorted(entities,key=lambda entity:entity['start'])
    labels = []
    inside = False
    previous_token_label = 'O'
    for token in tokens:
        token['label'] = 'O'
        for entity in entities:
            if entity['start'] <= token['start'] < entity['end'] or \
                    entity['start'] < token['end'] <= entity['end'] or \
                    token['start'] < entity['start'] < entity['end'] < token['end']:

                token['label'] = entity['label'].replace('-', '_')  # Because the ANN doesn't support tag with '-' in it
                break
            elif token['end'] < entity['start']:
                break

        if len(entities) == 0:
            entity = {'end': 0}
        if token['label'] == 'O':
            gold_label = 'O'
            inside = False
        elif inside and token['label'] == previous_token_label:
            gold_label = 'I-{0}'.format(token['label'])
        else:
            inside = True
            gold_label = 'B-{0}'.format(token['label'])
        if token['end'] == entity['end']:
            inside = False
        previous_token_label = token['label']
        token['label'] = gold_label
        labels.append(gold_label)
    return tokens,labels
        # token_sequence.append(token['text'])
        # label_sequence.append(gold_label)


def parse_brat(txt_file,type={'entity':'entity','Content':'content'}):
    assert (txt_file.endswith('.txt'))
    ann_file = txt_file[:-4]+'.ann'
    json_file = txt_file[:-4]+'.json'
    assert (os.path.exists(ann_file))
    assert (os.path.exists(json_file))
    json_data = json.load(codecs.open(json_file,'r','utf-8'))
    text_data = codecs.open(txt_file,'r','utf-8').read()
    idx = 0
    for obj in json_data:
        if len(obj['text'].strip())>0:
            start = text_data.index(obj['text'].strip(),idx)
            if start>=0:
                obj['start'] = start
                obj['end'] = start + len(obj['text'].strip())
                idx = obj['end']

    tokens = []
    for obj in json_data:
        tks = split_token(obj['text'],obj['start'])
        for token in tks:
            token['obj'] = obj
            tokens.append(token)

    entity_data = codecs.open(ann_file,'r','utf-8').readlines()
    n_content = 0
    labels={}
    for k,v in type.items():
        entities = get_entities(text_data,entity_data,type=v)
        for entity in entities:
            if entity['label'].endswith('Content'):
                n_content+=1
        tokens,labels[k] = merge_token_with_entity(tokens,entities)
        assert (len(tokens)==len(labels[k]))
        for token,label in zip(tokens,labels[k]):
            token[v]=label
    # for entity in tokens:
    #     print(entity)
    return tokens,labels,n_content

def get_entities_from_output(all_tokens,all_labels):
    tokens = []
    entitys = []

    entities = []
    start = 0
    end = 0
    sentence_with_entity = []
    token = ''
    previous_label = 'O'
    # sentence = utils_nlp.bioes_to_bio(sentence)
    for tk,label in zip(all_tokens,all_labels):
        # label = tk.get('label','O')
        text = tk['text']
        if label != 'O':
            label = label.split('-')
            prefix = label[0]
            if prefix == 'B' or previous_label != label[1]:
                if previous_label != 'O':
                    tokens.append(token)
                    entitys.append(previous_label)
                    sentence_with_entity.append((previous_label, token))
                    entity['end'] = pre_tk['end']
                    entity['label'] = previous_label
                    entities.append(entity)

                previous_label = label[1]
                token = text

                entity = {}
                entity['start'] = tk['start']
                entity['text'] = text

            else:
                token = token + ' ' + text

                entity['text'] += ' '+text
        else:
            if previous_label != 'O':
                tokens.append(token)
                entitys.append(previous_label)
                sentence_with_entity.append((previous_label, token))
                entity['end'] = pre_tk['end']
                entity['label'] = previous_label
                entities.append(entity)
                token = ''
                entity = {}
                entity['text']=''

            previous_label = 'O'
            sentence_with_entity.append(('O', text))
        pre_tk = tk
    return list(zip(tokens, entitys)), entities

def merge_entities(entities,contents):
    list_content = []
    for content in contents:
        c=content.copy()
        c['entities'] = []
        for entity in entities:
            if entity['label'] == 'Page_Index':
                continue
            if content['start']<=entity['start']< content['end'] \
                or content['start']<entity['end']<= content['end'] \
                or entity['start']<= content['start'] < content['end']<=entity['end']:
                c['entities'].append(entity)
        list_content.append(c)
    return list_content

def entities2json(entities):
    entities = sorted(entities,key=lambda x:x['start']*2+x['end'])
    result = {}
    result['person_details'] = {}
    result['objective'] = []
    result['education'] = []

    result['experience'] = []
    result['skill'] = {}
    result['awards'] = []
    result['hobbi'] = []
    result['other'] = {}
    person = {}
    result['skill'] = {}
    result['skill']['descriptions'] = []
    result['skill']['language'] = []
    result['skill']['programming'] = []
    other_title=None
    for entity in entities:
        if entity['label'] in ['Profile_Content']:
            for e in entity['entities']:
                person[e['label'].lower()] = e['text']
        elif entity['label'] in ['Objective_Content']:
            result['objective'].append(entity['text'])
        elif entity['label'] in ['Education_Content']:
            education={}
            for e in entity['entities']:
                if e['label'] in ['University', 'Time', 'Major', 'GPA','Certificate']:
                    education[e['label'].lower()] = e['text']
                else:
                    print(e)
            if len(education)>0:
                result['education'].append(education)
        elif entity['label'] in ['Award_Content']:
            result['awards'].append(entity['text'])
        elif entity['label'] in ['Experience_Content']:
            experience={}
            for e in entity['entities']:
                if e['label'] in ['Company','Time','Project','Programming','Client','Position','URL']:
                    experience[e['label'].lower()] = e['text']
                else:
                    print(e)
            if len(experience)>0:
                result['experience'].append(experience)
        elif entity['label'] in ['Skill_Content']:
            if len(entity['entities'])==0:
                result['skill']['descriptions'].append(e['text'])
            else:
                for e in entity['entities']:
                    if e['label'] in ['Programming']:
                        result['skill']['programming'].append(e['text'])
                    elif entity['label'] in ['Language']:
                        result['skill']['Language'].append(e['text'])
                    else:
                        print(e)
        elif entity['label'] in ['Programming']:
            result['skill']['programming'].append(entity['text'])
        elif entity['label'] in ['Language']:
            result['skill']['language'].append(entity['text'])
        elif entity['label'] in ['Hobbi_Content']:
            result['hobbi'].append(entity['text'])
        elif entity['label'] in ['Other_Title']:
            result['other'][entity['text']]=[]
            other_title = entity['text']
        elif entity['label'] in ['Other_Content'] and other_title!= None:
            result['other'][other_title].append(entity['text'])
        else:

            print(entity)

    result['person_details']=(person)
    return result

def obj_to_vector(obj):
    return [obj['h'],obj['x0'],obj['x1'],int(obj['is_title'])]

def vectorizer(tokens):
    vector = ([obj_to_vector(token['obj']) for token in tokens])
    # vector = np.nan(vector,axis=0)

    # for i in range(len(vector)):
    #     for j in range(len(vector[i])):
    #         if vector[i,j]==None:
    #             vector[i,j] = np.nan
    #
    # median = np.nanmedian(vector,axis=0)
    # for i in range(len(vector)):
    #     for j in range(len(vector[i])):
    #         if vector[i,j]==None:
    #             vector[i,j] = median[j]

    vector = np.divide(vector, np.max(vector, axis=0))
    return vector.tolist()

if __name__ == "__main__":
    # cluster_cv('../../ITSOL/data/pdf')
    # pdf2json('../../ITSOL/data/pdf/en','../../ITSOL/data/pdf/en/brat')
    # _,_,objs,_ = pdfreader.parse('cv/ITSOL_CV_IOS_ Ta Cuong.pdf')
    # for obj in objs:
    #     if obj.type == 'TextRect':
    #         for c in obj.childrens:
    #             print(c)
    #     else:
    #         print(obj)
    #
    tokens,labels = parse_brat('cv/brat/en/HR_Le_Thi_Minh_Hoa.txt')
    contents, e1 = get_entities_from_output(tokens, labels['Content'])
    entities,e2 = get_entities_from_output(tokens,labels['entity'])
    # for p in contents:
    #     print(p)
    # for p in entities:
    #     print(p)
    # for i in e1:
    #     print(i)
    #
    # print()
    # for i in e2:
    #     print(i)

    e1= merge_entities(e2,e1)
    e1 = entities2json(e1)
    for k,v in e1.items():
        if k in ['education','experience','objective']:
            print('+',k)
            for i in v:
                print(i)
        elif k in ['person_detail','skill']:
            print('+',k)
            for i,j in v.items():
                print('\t-',i,':',j)
        else:
            print(v)

