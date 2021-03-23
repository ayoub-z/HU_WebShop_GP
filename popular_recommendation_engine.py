import psycopg2
import random

#connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=12345')

#cursor
cur = con.cursor()


def pop_product_recommendation():
	'''
	This function generates a list containing 4 products from the table popular_products
	in the database. 
	'''

	cur.execute("SELECT * FROM popular_product")
	productlist = cur.fetchall()

	popular_products = []# will contain 4 random products from the list "pop_products"
	
	random.shuffle(productlist)
	for product in productlist[:4]:
		popular_products.append(product[0]) 
	return(popular_products)


