import pymongo


class Repository:
    myclient = pymongo.MongoClient(
        "mongodb+srv://Hwuang:q@cluster0.ot4kn.mongodb.net/bigdata_project?retryWrites=true&w=majority")
    mydb = myclient["ecommerce_electronic"]
    mycolection = mydb["product"]

    def deleteOne(self, id):
        print("[ Repository - deleteOne() ] id = ", id)
        self.mycolection.delete_one({"code": id})

    def getOne(self, id):
        print(f"[ Repository - getOne() ] id = '{id}'")
        item =  self.mycolection.find_one({"code": id}, {'_id': 0})
        # print("[ Repository - getOne() ] item = ", item)
        return item

    def getAll(self):
        print("[ Repository - getAll() ] self.collection = ", self.mycolection)
        items = list(self.mycolection.find({}))
        # print("[ Repository - getAll() ] items = ", items)
        return items

    def getByListId(self, ids):
        print("[ Repository - getByListId() ] ids = ", ids)
        return list(self.mycolection.find({"code": {"$in": ids}}, {'_id': 0}))

    def updateOne(self, query, value):
        print(f"[ Repository - updateOne() ] query = {query}, value = {value}")
        return self.mycolection.update_one(query, value)

    def getAllProuductOfCategory(self,categoryName):
        return list(self.mycolection.find({"category": categoryName}, {'_id': 0}))

