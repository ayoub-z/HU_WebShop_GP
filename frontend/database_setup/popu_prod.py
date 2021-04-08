import MongodbDAO
from db_connection import *


# informatie tonen over wat data
db = MongodbDAO.getMongoDB()
collectionsNames = db.list_collection_names()
for collectionName in collectionsNames:
    collection = db.get_collection(collectionName)

# zoeken
products = MongodbDAO.getDocuments("products")
profiles = MongodbDAO.getDocuments("profiles")
sessions = MongodbDAO.getDocuments("sessions")


def popu_prod():
    '''
    Pseudocode:
    Make table in PostgreSQL named 'Populairste_prod', if table doesn't exist already.
    Make dict 'popu_dict'.
    Loop through all sessions
    Loop through all product in order per session
    Check if product, already exists in dict.
    If product doesn't yet exist, add key to dict.
    If product DOES exist, +1 to key value.
    Once looping is done, order the dict from highest to lowest key.value.
    Insert dict into PostgreSQL.
    Populairste_prod containts the following:
    Primary key  RANK, which will be auto incrementing, meaning we don't have to insert rank.
    productid, this will be the ID of the product.
    count, this will be the amount of times a product was found in 'orders'. ( This does not have any significance for any recommendations being made in the future. )
    '''

    cur.execute(
        "CREATE TABLE IF NOT EXISTS Populairste_prod (Rank SERIAL,productid varchar(255) NOT NULL,count int NOT NULL,PRIMARY KEY (Rank));")
    popu_dict = {}

    keyerror = 0

    # Filter MongoDB Sessions to not retreive excess information. Only 'Order' Is relevant in this function.
    sess_filter = {"order": 1}
    sessions_filtered = MongodbDAO.getCollection("sessions").find({}, sess_filter, no_cursor_timeout=True)
    # loop through filtered sessions
    for session in sessions_filtered:
        # try & Except to filter out keyerrors ( meaning order doesn't exist in a session )
        try:
            if session['order'] != None:
                # loop through products in the order. Add the product to the dict if it doesn't exists yet. If it exists, +1 to value.
                for product in session['order']['products']:
                    for key, value in product.items():
                        if value in popu_dict:
                            popu_dict[str(value)] += 1
                        elif value not in popu_dict:
                            popu_dict[str(value)] = 1
        except KeyError:
            keyerror += 1
    print(f' Amount of keyerrors: {keyerror}')

    # Reverse sort the dict, meaning value will go from high to low.
    popu_dict = sorted(popu_dict.items(), key=lambda x: x[1], reverse=True)

    # insert data into postgreSQL
    for product in popu_dict:
        inserttuple = (product[0], product[1])
        cur.execute("INSERT INTO populairste_prod ( productid, count) VALUES ( %s, %s )", inserttuple)


popu_prod()
con.commit()
