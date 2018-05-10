import json
import os

from .ner import dataset,lstm_crf,utils,utils_nlp
from langdetect import detect_langs
from .. import preprocess

class Extraction(object):
    def __init__(self):
        dir_model = os.path.join(os.path.dirname(__file__),'model')
        model_path = {}
        model_path['vi'] = os.path.join(dir_model,'vi_extend_1')
        model_path['en'] = os.path.join(dir_model,'en')
        # model_path['vi']['content'] = os.path.join(dir_model,'vi')
        # model_path['vi']['entity'] = 'ai_model/model/vi/entity'
        # model_path['vi']['vocab'] =  os.path.join(dir_model,'vi','vocab.json')
        # model_path['en']['content'] =  os.path.join(dir_model,'en')
        # model_path['en']['entity'] = 'ai_model/model/en/entity'
        # model_path['en']['vocab'] = os.path.join(dir_model,'en','vocab.json')

        self.model = {}
        for lang,path in model_path.items():
            print('Load model {0}...'.format(lang))
            self.model[lang]={}


            vocab = dataset.Dataset()
            vocab.load(os.path.join(path,'vocab.json'))
            self.model[lang]['vocab'] = vocab

            parameters = json.load(open(os.path.join(path, 'parameters.json'), 'r'))

            token_embedding_dimension = parameters['token_embedding_dimension']
            character_lstm_hidden_state_dimension = parameters['character_lstm_hidden_state_dimension']
            token_lstm_hidden_state_dimension = parameters['token_lstm_hidden_state_dimension']
            character_embedding_dimension = parameters['character_embedding_dimension']
            vector_extend_dimension = parameters.get('vector_extend_dimension', vocab.size_pattern_vector)
            self.model[lang]['use_extend_vector']= not ( vector_extend_dimension == vocab.size_pattern_vector)

            model_content = lstm_crf.BLSTM_CRF(vocab, token_embedding_dimension=token_embedding_dimension,
                                               character_lstm_hidden_state_dimension=character_lstm_hidden_state_dimension,
                                               token_lstm_hidden_state_dimension=token_lstm_hidden_state_dimension,
                                               character_embedding_dimension=character_embedding_dimension,
                                               vector_extend_dimension=vector_extend_dimension)
            model_content.load_model(os.path.join(path,'ner_content.ckpt'))
            self.model[lang]['content'] = model_content

            model_entity = lstm_crf.BLSTM_CRF(vocab, token_embedding_dimension=token_embedding_dimension,
                                               character_lstm_hidden_state_dimension=character_lstm_hidden_state_dimension,
                                               token_lstm_hidden_state_dimension=token_lstm_hidden_state_dimension,
                                               character_embedding_dimension=character_embedding_dimension,
                                              vector_extend_dimension=vector_extend_dimension)
            model_entity.load_model( os.path.join(path, 'ner_entity.ckpt'))
            self.model[lang]['entity'] = model_entity
            print('Done.')


    def predict(self,path_file):
        tokens,image = preprocess.pdf2tokens(path_file)
        token_texts = [[token['text'] for token in tokens]]
        lang = str(detect_langs(' '.join(token_texts[0]))[0])[:2]
        result = {}
        result['language_cv'] = lang
        result['image'] = image
        if lang in self.model.keys():

            token_texts = [[token['text'] for token in tokens]]
            vector_obj = preprocess.vectorizer(tokens)
            token_indices, character_indices_padded, token_lengths, pattern = self.model[lang]['vocab'].transform(token_texts)
            if self.model[lang]['use_extend_vector']:
                for i in range(len(pattern[0])):
                    pattern[0][i].extend(vector_obj[i])

            pre_content = self.model[lang]['content'].predict( token_indices, character_indices_padded, token_lengths,
                                        pattern)

            pre_entity = self.model[lang]['entity'].predict( token_indices, character_indices_padded, token_lengths,
                                              pattern)
            pre_content = [self.model[lang]['vocab'].labels[i] for i in pre_content[0]]
            pre_entity = [self.model[lang]['vocab'].labels[i] for i in pre_entity[0]]
            _, e1 = preprocess.get_entities_from_output(tokens, pre_content)
            _, e2 = preprocess.get_entities_from_output(tokens, pre_entity)

            e1 = preprocess.merge_entities(e2, e1)
            e1 = preprocess.entities2json(e1)
            result.update(e1)
            return result

        return result