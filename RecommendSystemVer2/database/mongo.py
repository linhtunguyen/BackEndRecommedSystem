import pymongo


class Repository:
    myclient = pymongo.MongoClient(
        "mongodb+srv://Hwuang:q@cluster0.ot4kn.mongodb.net/bigdata_project?retryWrites=true&w=majority")
    mydb = myclient["ecommerce_electronic"]
    mycolection = mydb["product"]

    def getOne(self, id):
        print("[ Repository - getOne() ] id = ", id)
        item =  self.mycolection.find_one({"code": id}, {'_id': 0})
        print("[ Repository - getOne() ] item = ", item)
        return item

    def getAll(self):
        print("[ Repository - getAll() ] self.collection = ", self.mycolection)
        items = list(self.mycolection.find({}))
        print("[ Repository - getAll() ] items = ", items)
        return items

