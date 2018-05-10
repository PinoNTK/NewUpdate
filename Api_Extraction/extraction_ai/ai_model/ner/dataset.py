import codecs
import glob

import os

import numpy as np
import collections

import sklearn.preprocessing

from . import utils_re,utils,utils_nlp

import en_core_web_sm
import json





class Dataset(object):
    expressions = [
        r"[A-Z]",
        r"[0-9]{10,12}",
        r"[0-9]+",
        r"(?:[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])+",
        r"([a-zA-Z0-9][a-zA-Z0-9_.+-]*@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)",
        r"(?:ftp|http|https)?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        r"[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+",
        r"(?:[0-9]+\.)+[0-9]+",
        r"(?:[0-9]+\.){3}[0-9]+",
        r"(?:[0-9]+\.){5}[0-9]+",
        r"(?:AS|as)[0-9]+",
        r"(?:CVE|exploit)",
        r"(?:HK|hk)[a-zA-Z0-9/]+"]


    def __init__(self, expressions=None):
        self.token2index = {}
        self.tokens = []
        self.characters = []
        self.character2index = {}
        self.UNK = 'UNK'
        self.UNK_INDEX = 0
        self.tokens.append(self.UNK)
        self.token2index[self.UNK] = 0
        self.PADDING_INDEX = 0
        self.characters.append('pad')
        # self.token2vector = token_to_vector
        # self.dictionary = (token_to_vector.keys())
        # self.token2vector[self.UNK] = np.zeros([embedding_dim])

        # self.embedding_dim = embedding_dim
        self.label2index = {}
        self.labels = []
        self.add_label('O')
        # self.nlp = en_core_web_sm.load()
        self.verbose = False
        self.number_of_classes = 1

        if expressions != None:
            self.expressions = []
            for exp in expressions:
                self.expressions.append(exp)
        else:
            self.expressions = [
                r"[A-Z]",
                r"[0-9]{10,12}",
                r"[0-9]+",
                r"(?:[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])+",
                r"([a-zA-Z0-9][a-zA-Z0-9_.+-]*@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)",
                r"(?:ftp|http|https)?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                r"[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+",
                r"(?:[0-9]+\.)+[0-9]+",
                r"(?:[0-9]+\.){3}[0-9]+",
                r"(?:[0-9]+\.){5}[0-9]+",
                r"(?:AS|as)[0-9]+",
                r"(?:CVE|exploit)",
                r"(?:HK|hk)[a-zA-Z0-9/]+"]
        self.size_pattern_vector = len(self.expressions)
        self.vocabulary_size = len(self.tokens)


    def add_token(self, token ,token_to_vector):
        lower = token.lower()
        if lower in token_to_vector.keys():
            if lower not in self.token2index.keys():
                self.token2index[lower] = len(self.tokens)
                self.tokens.append(lower)
                self.vocabulary_size = len(self.tokens)

        for char in list(token):
            self.add_character(char)

    def add_character(self, char):
        if char not in self.character2index.keys():
            self.character2index[char] = len(self.characters)
            self.characters.append(char)
            self.alphabet_size = len(self.characters)

    def add_label(self, label):
        if label not in self.label2index.keys():
            self.label2index[label] = len(self.label2index)
            self.labels.append(label)
            self.number_of_classes = len(self.labels) + 1

    def get_embedding(self, token2vector, embedding_dim):
        unk_vector = np.zeros([embedding_dim])
        return np.array([token2vector.get(token, unk_vector) for token in self.tokens])

    def build_vocabulary(self, tokens ,token_to_vector ):
        for sequence in tokens:
            for token in sequence:
                lower = token.lower()
                if lower in token_to_vector.keys():
                    if lower not in self.token2index.keys():
                        self.token2index[lower] = len(self.tokens)
                        self.tokens.append(lower)
                        self.vocabulary_size = len(self.tokens)

                for char in list(token):
                    self.add_character(char)

    def build_labels(self, labels):
        for label_sequence in labels:
            for label in label_sequence:
                self.add_label(label)

    def transform(self, tokens, labels=None):

        pattern = [[utils_re.get_pattern(token, self.expressions) for token in sequence] for sequence in tokens]
        token_indices = []
        characters = []
        character_indices = []
        token_lengths = []
        character_indices_padded = []
        for token_sequence in tokens:
            token_indices.append(
                [self.token2index.get(token.lower(), self.UNK_INDEX) for token in token_sequence])
            characters.append([list(token) for token in token_sequence])
            character_indices.append(
                [[self.character2index.get(character, 0) for character in token] for token in token_sequence])
            token_lengths.append([len(token) for token in token_sequence])
            longest_token_length_in_sequence = max(token_lengths[-1])
            character_indices_padded.append(
                [utils.pad_list(temp_token_indices, longest_token_length_in_sequence, self.PADDING_INDEX)
                 for temp_token_indices in character_indices[-1]])

        if labels == None:
            return token_indices, character_indices_padded, token_lengths, pattern
        label_indices = []

        for label_sequence in labels:
            label_indices.append([self.label2index.get(label,self.label2index['O']) for label in label_sequence])

        if self.verbose:
            print('token_lengths[\'train\'][0][0:10]: {0}'.format(token_lengths[0][0:10]))
        if self.verbose:
            print('characters[\'train\'][0][0:10]: {0}'.format(characters[0][0:10]))
        if self.verbose:
            print('token_indices[\'train\'][0:10]: {0}'.format(token_indices[0:10]))
        if self.verbose:
            print('label_indices[\'train\'][0:10]: {0}'.format(label_indices[0:10]))
        if self.verbose:
            print('character_indices[\'train\'][0][0:10]: {0}'.format(character_indices[0][0:10]))
        if self.verbose:
            print('character_indices_padded[\'train\'][0][0:10]: {0}'.format(
                character_indices_padded[0][0:10]))  # Vectorize the labels
        # [Numpy 1-hot array](http://stackoverflow.com/a/42263603/395857)
        label_binarizer = sklearn.preprocessing.LabelBinarizer()
        label_binarizer.fit(range(len(self.labels) + 1))

        label_vector_indices = []
        for label_indices_sequence in label_indices:
            label_vector_indices.append(label_binarizer.transform(label_indices_sequence))
        # self.number_of_classes = len(self.labels) + 1

        if self.verbose:
            print('label_vector_indices[\'train\'][0:2]: {0}'.format(label_vector_indices['train'][0:2]))
        if self.verbose:
            print('len(label_vector_indices[\'train\']): {0}'.format(len(label_vector_indices['train'])))

        return token_indices, character_indices_padded, token_lengths, pattern, label_indices, label_vector_indices

    def to_json(self,pathfile):
        with codecs.open(pathfile,'w') as output:
            output.write(json.dumps(self.__dict__))
        return json.dumps(self.__dict__)
    def load(self,pathfile):
        json_str = u'' + codecs.open(pathfile, 'r').read()
        json_dict = json.loads(json_str)
        self.__dict__ = json_dict
    @classmethod
    def from_json(cls, pathfile):
        json_str = codecs.open(pathfile,'r').read()
        # print(json_str)
        json_dict = json.loads(json_str)
        # print(json_dict)
        return cls(json_dict)