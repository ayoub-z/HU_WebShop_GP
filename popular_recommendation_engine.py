import psycopg2
import random

#connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=12345')

#cursor
cur = con.cursor()



def pop_product_recommendation():
	'''
	This function generates a list containing 4 products from the table populaireste_prod
	in the database. 
	'''

	cur.execute("SELECT * FROM populaireste_prod")
	productlist = cur.fetchall()

	productlist = productlist[:100] # limit to only the top 100 products
	popular_products = []# will contain 4 random products from the list "pop_products"
	
	# shuffle list and pick the first 4 products
	random.shuffle(productlist)
	for product in productlist[:4]:
		popular_products.append(product[1]) 
	return(popular_products)




