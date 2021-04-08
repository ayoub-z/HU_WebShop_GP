import pymongo

def getMongoDB(mongoConnectString = "mongodb://localhost:27017/",databaseName = "huwebshop"):
	myClient = pymongo.MongoClient(mongoConnectString)
	return myClient[databaseName]

def getCollection(collectionName):
	'''Get a collection from the mongodb huwebshop'''
	return getMongoDB().get_collection(collectionName)

def getDocuments(collectionName, filter = {}):
	return getCollection(collectionName).find(filter,no_cursor_timeout=True)