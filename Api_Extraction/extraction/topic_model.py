
import pickle

import os

from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
import numpy as np
import pandas as pd
from . import utils_nlp

class ClassificationTopic(object):
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english',ngram_range=[1,3],max_df=0.7,min_df=0.05)
        gnb = GaussianNB()
        svc = SVC(kernel='rbf', gamma=1, C=10)
        mnb = MultinomialNB()
        rdf = RandomForestClassifier(n_estimators=20)
        mlp = MLPClassifier()
        model = VotingClassifier(estimators=[('mnb', mnb), ('gnb', gnb), ('rdf', rdf), ('svm', svc), ('mlp', mlp)],
                                 voting='hard')
        self.svc =  model
        self.label_unique = []


    def fit(self,texts,labels):
        texts = [utils_nlp.clean_string(text) for text in texts]
        x = self.vectorizer.fit_transform(texts).toarray()
        labels = [str(s).lower() for s in labels.str.replace('*', '')]
        labels = pd.DataFrame(data={'output': labels})['output']
        self.label_unique = labels.unique()
        d={}
        for i,label in enumerate(self.label_unique):
            d[label]=i
        y = labels.map(d)
        self.svc.fit(x,y)
        print(classification_report(y,self.svc.predict(x)))
    def predict(self,texts):
        texts = [utils_nlp.clean_string(text) for text in texts]
        x= self.vectorizer.transform(texts).toarray()
        return texts,[self.label_unique[i] for i in self.svc.predict(x)]
    def save(self,file):
        # pickle.dump(self.vectorizer,open(os.path.join(folder,'vectorizer.pickle'),'wb'))
        pickle.dump(self,open(file,'wb'))
def load(file):
        # self.vectorizer = pickle.load(open(os.path.join(folder,'vectorizer.pickle'),'rb'))
    return  pickle.load(open(file,'rb'))


def merge_topic(texts,labels,cluster_obj):
    return texts,labels,cluster_obj