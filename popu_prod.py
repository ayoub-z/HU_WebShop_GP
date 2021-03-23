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
	Once looping is done, order the dict from highest to lowest key.value.
	Insert dict into PostgreSQL.


	Populairste_prod containts the following:
	Primary key  RANK, which will be auto incrementing, meaning we don't have to insert rank.
	productid, this will be the ID of the product.
	count, this will be the amount of times a product was found in 'orders'. ( This does not have any significance for any recommendations being made in the future. )
	'''

	cur.execute("CREATE TABLE IF NOT EXISTS Populairste_prod (Rank SERIAL,productid varchar(255) NOT NULL,count int NOT NULL,PRIMARY KEY (Rank));")
	popu_dict = {}



popu_prod()

con.commit()