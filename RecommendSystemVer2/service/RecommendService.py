import logging

import database.mongo as mg
import model.Tfidf as tf

class RecommenderService:
    repo = mg.Repository()

    def __init__(self):
        items = self.repo.getAll()
        itemDict = {'code': [], 'description': []}
        for i in items:
            itemDict['code'].append(i['code'])
            itemDict['description'].append(i['description'])

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
        relevantItems = self.storage.searchByQuery(query)
        return relevantItems