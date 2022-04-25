import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
# from nltk.corpus import stopwords
import csv
import re
from underthesea import word_tokenize
import string

def clean_str(string):
    string = re.sub(
        r"[^aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0-9(),!?\'\`]",
        " ", string)
    return string.strip()

def text_lowercase(string):
    return string.lower()


def tokenize(strings):
    return word_tokenize(strings, format="text")


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def remove_stopwords(strings):
    strings = strings.split()
    f = open('./vietnamese-stopwords.txt', 'r', encoding='utf-16')
    stopwords = f.readlines()
    stop_words = [s.replace("\n", '') for s in stopwords]
    doc_words = []
    for word in strings:
        if word not in stop_words:
            doc_words.append(word)
    doc_str = ' '.join(doc_words).strip()
    return doc_str

def text_preprocessing(doc):
    docAfterPreprocess=[]
    for strings in doc:
        temp = clean_str(strings)
        temp = remove_punctuation(temp)
        temp = text_lowercase(temp)
        temp = tokenize(temp)
        temp = remove_stopwords(temp)
        docAfterPreprocess.append(temp)
    return docAfterPreprocess

ds = pd.read_csv("./database/laptop_all.csv")
# stop = list(stopwords.words('Vietnamese'))
# tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words=set(stop))
class SimilarityProduct:
    def __init__(self):
        self.results = {}
    def getSimilaryUseTfIdf(self):
        tf = TfidfVectorizer(ngram_range=(1, 3), min_df=0,max_features=5000,sublinear_tf=True)
        tfidf_matrix = tf.fit_transform(text_preprocessing(ds['full_name'].values.astype('U')))
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
        # results = {}
        for idx, row in ds.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], ds['code'][i]) for i in similar_indices]
            self.results[row['code']] = similar_items[1:]
            print('done!')


    def item(id):
        return ds.loc[ds['code'] == id]['full_name'].tolist()[0].split(' - ')[0]


    # Just reads the results out of the dictionary.
    # productRec=[]
    def recommend(self,item_id, num):
        productRec=[]
        # print('id',item_id)
        # print('results', results)
        print("Recommending " + str(num) + " products similar to " + str(item_id) + "...")
        print("-------")
        recs = self.results[item_id][:num]
        for rec in recs:
            print("Recommended: " + str(int(rec[1])) + " (score:" + str(rec[0]) + ")")
            # print("Recommendeding: " + str(rec))
            productRec.append(str(int(rec[1])))
        # print('pr' ,productRec)
        return productRec

    def getInforProductRecommended(listProductCode):
        listInforProduct=[]
        with open('/database/laptop_all.csv',encoding="utf8") as f:
            csv_reader1 = csv.reader(f)
            header = next(csv_reader1)
            csv_reader=list(csv_reader1)
            for i in csv_reader:
                for j in listProductCode:
                    if str(i[0]) == j:
                        listInforProduct.append({'code':i[0],'name':i[1],'price':i[2],'category':i[3],'brand':i[4]})
        print('re',listInforProduct)
        return listInforProduct
# recommend(item_id=220042001424, num=10)
# getInforProductRecommended(recommend(item_id=220042001424, num=10))
