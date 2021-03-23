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

	random_products = []# will contain 4 random products from the list "pop_products"
	
	for i in range (0,4): # picks 4 random products and appends them to a list
		random_choice = random.choice(pop_products) 
		random_products.append(random_choice[0]) 
	return(random_products)