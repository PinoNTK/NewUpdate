
from . import topic_model
from . import pdf_reader
from . import utils_nlp
from . import utils_file
from . import vi
from . import en
from . import requirment
import datefinder
import os
from recruitment_recommender_system.settings import BASE_DIR

BASE_DIR = '../..'

# topic = topic_model.ClassificationTopic()
# df = pd.read_excel(os.path.join(dir_path,'data/topic_train_vi.xlsx'))
# topic.fit(df['vi'],df['label'])
# topic.save(os.path.join(dir_path,'model/topic_model_vi.pickle'))
class Extraction(object):
    def __init__(self,base_dir):
        dir_path = os.path.join(base_dir, 'Api_Extraction/extraction')
        self.topic={}
        self.topic['en'] = topic_model.load(os.path.join(dir_path,'model/topic_model_en.pickle'))
        self.topic['vi'] = topic_model.load(os.path.join(dir_path,'model/topic_model_vi.pickle'))
    # topics = ['personal_details','objective','experience', 'education','language','skills','others','awards']
    def parse_cv(self,pathfile):
        pathfile = utils_file.doc_to_pdf(pathfile)
        if not pathfile:
            return "Chỉ sử lí file pdf và word"
        texts,cluster_obj, tables ,images = pdf_reader.parse(pathfile)
        # print(texts)
        # return texts
        result = {}
        langs = utils_nlp.classification_language(texts)
        result['language_cv']=langs
        result['image'] = images
        # return langs
        # texts = [text for text,lang in zip(texts,langs) if lang=='en']  # Chỉ xử lý với tiếng anh
        if langs=='en':
            texts , topics = self.topic['en'].predict(texts)

            result['person_details'] = en.extract_detail(texts, topics,cluster_obj)
            result['education'] = en.extract_education(texts, topics,cluster_obj)
            result['skills'] = en.extract_skill(texts, topics)
            result['experience'] = en.extract_project(texts, topics,cluster_obj)
            result['other'] = en.extract_other(texts, topics,cluster_obj)

        elif langs=='vi':
            texts, topics = self.topic['vi'].predict(texts)

            result['person_details'] = vi.extract_detail(texts, topics, cluster_obj)
            result['education'] = vi.extract_education(texts, topics,cluster_obj)
            result['skills'] = vi.extract_skill(texts, topics)
            result['experience'] = vi.extract_project(texts, topics,cluster_obj)
            result['other'] = vi.extract_other(texts, topics,cluster_obj)
        else:
            return {}
            return "Chỉ sử lí được CV tiếng anh và tiếng Việt"

        if result['person_details']['birth_day']!=None:
            matches = datefinder.find_dates(result['person_details']['birth_day'])
            for match in matches:
                # print('birth_day', match.date())
                result['person_details']['birth_day'] =str(match.date())

        return result


    def parse_requirment(self,text):
        return requirment.parse(text)
# print(parse_cv('../cv/le_thi_minh_hoa.pdf'))
