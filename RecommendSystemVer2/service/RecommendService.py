import logging

import database.mongo as mg
import model.Tfidf as tf

class RecommenderService:
    repo = mg.Repository()

    def __init__(self):
        items = self.repo.getAll()
        itemDict = {'code': [], 'description': []}
        f_items = []
        for i in items:
            if 'MoTa' not in i:
                f_items.append(i)
                continue

            itemDict['code'].append(i['code'])
            itemDict['description'].append(i['MoTa'])

        print(f_items)
        self.storage = tf.Storage(itemDict)

    def getAll(self):
        print("[ RecommenderService - getAll() ] repo = ", self.repo)
        return self.repo.getAll()

    def getOne(self, id):
        print("[ RecommenderService - getOne() ] id = ", id)
        return self.repo.getOne(id)

    def getOneTest(self, id):
        print("[ RecommenderService - getOne() ] id = ", id)
        return self.repo.getOne(id)["name"]

    def getRelevantProduct(self, id):
        print("[ RecommenderService - getRelevantProduct() ] id = ", id)
        currentItem = self.repo.getOne(id)

        if currentItem is None:
            logging.exception("Item id not found: ", id)
            raise "Item not found"

        relevantItems = currentItem["relevantItems"]
        return relevantItems

    def getProductByQuery(self, query):
        print("[ RecommenderService - getProductByQuery() ] query = ", query)
        relevantItemsCode = self.storage.searchByQuery(query)

        items = self.repo.getByListId(relevantItemsCode)

        return items

    def updateItemRelevantItems(self):
        items = self.repo.getAll()
        for i in items:
            relevantItemsCode = self.storage.searchByQuery(i['MoTa'])
            query = {"code": i["code"]}
            val = {"$set": {"relative": relevantItemsCode}}
            self.repo.updateOne(query, val)

        return

    def getItemRelative(self, id):
        item = self.repo.getOne(id)

        if 'relative' not in item:
            raise 'Item doesnt have relative'

        relative = self.repo.getByListId(item['relative'])
        return relative

    def getListProductByCategory(self,categoyName):
        return self.repo.getAllProuductOfCategory(categoyName)
