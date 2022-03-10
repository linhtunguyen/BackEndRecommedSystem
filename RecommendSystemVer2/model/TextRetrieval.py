import numpy as np
import sklearn
import underthesea
import json
import os
from tqdm.autonotebook import tqdm
from glob import glob
from pprint import pprint
import nltk
from underthesea import word_tokenize
from sklearn.decomposition import TruncatedSVD
import math
import sklearn
from difflib import get_close_matches

import pandas as pd
df = pd.read_csv('./database/laptop_all.csv')

def clean_laptop_name(name):
    name = str(name).lower()
    return name

items = []

for index, row in df.iterrows():
    items.append(str(row['code']) + '\n' + clean_laptop_name(row['full_name']))


class Tfidf:
    def __init__(self):
        self.corpus = {}
        self.corpus_counter = {}
        self.corpus_dict = []
        self.corpus_len = 0

    '''
    Xây dựng TF-IDF cho danh sách documents nhận đuợc
    documents: list<string>
    '''

    def fit_data(self, documents):
        #         print(type(documents))
        #         if type(documents) != "list":
        #             raise ValueError('documents must be type of list')

        #         đếm số lần xuất hiện của mỗi từ
        for d in documents:
            #             tokens = word_tokenize(d, format='text').split()
            tokens = d.split()
            self.corpus_len += 1
            for t in tokens:
                if t in self.corpus_counter.keys():
                    self.corpus_counter[t] += 1
                else:
                    self.corpus_counter[t] = 1

        for k in self.corpus_counter.keys():
            self.corpus_dict.append(k)

    def print_data(self):
        print(self.corpus_counter)
        print(len(self.corpus_counter))

    def get_tfidf(self, string):
        string = string.lower()
        doc_counter = {}
        k = 2
        tokens = string.split()
        #         tokens = word_tokenize(string, format='text').split()
        for t in tokens:
            if t in doc_counter.keys():
                doc_counter[t] += 1
            else:
                doc_counter[t] = 1

        vector_len = len(self.corpus_counter)
        tfidf_vector = np.zeros((vector_len,))
        for i, key in enumerate(self.corpus_counter.keys()):
            if key in doc_counter.keys():
                tf = (k + 1) * doc_counter[key] / (k + doc_counter[key])
                idf = math.log((self.corpus_len + 1) / (self.corpus_counter[key]))
                tfidf_vector[i] = tf * idf
        return tfidf_vector

    '''
    Xử lý query user đưa vào
    returns: list query mà hệ thống cho là người dùng muốn sử dụng để tìm kiếm
    '''

    def preprocess_query(self, query):
        tokens = query.split()
        refined = []
        # correct lại từng từ trong query
        for t in tokens:
            if t in self.corpus_counter.keys():
                refined.append(t)
                continue

            substitute = get_close_matches(t, self.corpus_dict, n=1, cutoff=0.5)
            if len(substitute) > 0:

                refined.append(substitute[0])
            else:
                refined.append(t)

        return " ".join(refined)
        # thêm bigram


class Storage:
    def __init__(self):
        self.tfidf_space = []
        self.tfidf = Tfidf()
        self.svd = TruncatedSVD(n_components=256)
        self.items = []

    '''
    items: list<string>
    '''

    def fit_data(self, items):
        self.tfidf.fit_data(items)

        for i in items:
            self.tfidf_space.append(self.tfidf.get_tfidf(i))
            self.items.append(i)

    #         self.svd.fit(self.tfidf_space)
    #         self.svd_tfidf_vector = self.svd.transform(self.tfidf_space)

    '''
    item: string
    '''

    def get_similiar_items(self, item):
        listPro=[]
        query_vector = self.tfidf.get_tfidf(item)
        query_vector = np.reshape(query_vector, (1, -1))
        # search
        sim_maxtrix = sklearn.metrics.pairwise.cosine_similarity(query_vector, self.tfidf_space)
        sim_maxtrix = np.reshape(sim_maxtrix, (-1,))
        idx = (-sim_maxtrix).argsort()[:30]
        for _id in idx:
            # print(_id, sim_maxtrix[_id])
            #             print(newItems[_id]['name'].upper())
            print('code : ',self.items[_id])
            listPro.append(self.items[_id][0:12])
        return listPro
    def evaluate_query(self, query):

        query_vector = self.tfidf.get_tfidf(query)
        query_vector = np.reshape(query_vector, (1, -1))
        sim_maxtrix = sklearn.metrics.pairwise.cosine_similarity(query_vector, self.tfidf_space)
        sim_maxtrix = np.reshape(sim_maxtrix, (-1,))

        result = []
        for idx, val in enumerate(sim_maxtrix):
            if val > 0.2:
                result.append(self.items[idx].split()[0])

        return result


def getProductItem(query_string):
    s = Storage()
    item_descriptions = []
    for i in items:
        item_descriptions.append(i)
    s.fit_data(item_descriptions)
    return s.get_similiar_items(query_string)

