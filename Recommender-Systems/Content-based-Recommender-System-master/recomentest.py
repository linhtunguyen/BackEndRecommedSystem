import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords
import csv

ds = pd.read_csv(
    "./laptop_all.csv")
# stop = list(stopwords.words('Vietnamese'))
# tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words=set(stop))
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
print('tf',tf)
tfidf_matrix = tf.fit_transform(ds['full_name'].values.astype('U'))
print('tfidf_matrix',tfidf_matrix)
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['code'][i]) for i in similar_indices]

    results[row['code']] = similar_items[1:]

print('done!')


def item(id):
    return ds.loc[ds['code'] == id]['full_name'].tolist()[0].split(' - ')[0]


# Just reads the results out of the dictionary.
# productRec=[]
def recommend(item_id, num):
    productRec=[]
    # print('id',item_id)
    # print('results', results)
    print("Recommending " + str(num) + " products similar to " + str(item_id) + "...")
    print("-------")
    recs = results[item_id][:num]
    for rec in recs:
        print("Recommended: " + str(int(rec[1])) + " (score:" + str(rec[0]) + ")")
        # print("Recommendeding: " + str(rec))
        productRec.append(str(int(rec[1])))
    # print('pr' ,productRec)
    return productRec

def getInforProductRecommended(listProductCode):
    listInforProduct=[]
    with open('./laptop_all.csv',encoding="utf8") as f:
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
getInforProductRecommended(recommend(item_id=220042001424, num=10))
