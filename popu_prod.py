import MongodbDAO
import psycopg2

#connect to the db
con = psycopg2.connect('host=localhost dbname=hu_webshop user=postgres password=123')

# informatie tonen over wat data
db = MongodbDAO.getMongoDB()
collectionsNames = db.list_collection_names()
for collectionName in collectionsNames:
	collection = db.get_collection(collectionName)

#cursor
cur = con.cursor()

#zoeken
products = MongodbDAO.getDocuments("products")
profiles = MongodbDAO.getDocuments("profiles")
sessions = MongodbDAO.getDocuments("sessions")


def popu_prod():
	'''
	Pseudocode:
	Make table in PostgreSQL named 'Populairste_prod', if table doesn't exist already.
	Make dict 'popu_dict'.
	Loop through all sessions
	Loop through all orders per session
	Check if product in order, already exists in dict.
	If product doesn't yet exist, add key to dict.
	If product DOES exist, +1 to key value.
	Once looping is done, order the list from highest to lowest value.

	'''




popu_prod()

con.commit()