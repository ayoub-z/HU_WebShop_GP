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
	pop_products = cur.fetchall()

	random_products = []# list that will contain the initial_product and 4 other products for recommendation
	
	for i in range (0,4): # repeats 4 times
		random_choice = random.choice(pop_products) # picks 4 random products from pre-filtered list
		random_products.append(random_choice[0]) # adds the 4 picked products to product list
	return(random_products)