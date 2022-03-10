import pymongo
# import sys
# sys.path.append('/Content-based-Recommender-System-master/model/RecommendClicked.py')
# import RecommendClicked as recommending
import model.RecommendClicked as RecommendClicked
import model.TextRetrieval as TextRetrieval

myclient = pymongo.MongoClient("mongodb+srv://Hwuang:q@cluster0.ot4kn.mongodb.net/bigdata_project?retryWrites=true&w=majority")
mydb = myclient["ecommerce_electronic"]
mycolection = mydb["product"]

def recommendWhenClickToAProduct(item_id):
    listProductÌnfor = []
    recommending=RecommendClicked.SimilarityProduct()
    recommending.getSimilaryUseTfIdf()
    listProductCode = recommending.recommend(int(item_id), num=10)
    for proCode in listProductCode:
        result = mycolection.find_one({"code": proCode}, {'_id': 0})
        listProductÌnfor.append(result)
    return listProductÌnfor

def recommendByQuery(query_string):
    listProductÌnfor = []
    recomendByQuery=TextRetrieval.Storage()
    item_descriptions = []
    for i in TextRetrieval.items:
        item_descriptions.append(i)
    recomendByQuery.fit_data(item_descriptions)
    listProductCode = recomendByQuery.get_similiar_items(query_string)
    for proCode in listProductCode:
        result = mycolection.find_one({"code": proCode}, {'_id': 0})
        listProductÌnfor.append(result)
    return listProductÌnfor