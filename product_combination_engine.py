import psycopg2
import random

#connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=12345')

#cursor
cur = con.cursor()

def shopping_cart_products(product_id):
	'''
	Function takes a product_id as input and goes through all shopping carts that contain
	this product_id and retrieves all other products in shopping cart, besides this product_id.
	It then returns the 4 products that have been the most commonly found.
	'''
	product_id = str(product_id) # turn product_id into string

	# sql query that finds all product_ids in the table "product_order" which are in the same "orderorderid" as the given product_id
	cur.execute("SELECT product_id FROM product_order WHERE orderorderid in (SELECT orderorderid from product_order where %s in (product_id))", (product_id,))
	shopping_cart_products = cur.fetchall() # inputs all found products as list into this variable

	dict_shopping_cart_products = {} # dictionary that will keep track of the amount of times a product has been found

	for product in shopping_cart_products:
		# add product to dictionary if it's not in it and product isn't the same as initial product_id
		if product[0] not in dict_shopping_cart_products and product[0] != product_id:
			dict_shopping_cart_products[product[0]] = 1
		# add +1 to product counter in dictionary if product in dictionary and product isn't the same as initial product_id
		if product[0] in dict_shopping_cart_products and product[0] != product_id:
			dict_shopping_cart_products[product[0]] += 1

	# sorts dictionary from top to bottom and picks only the top 4 results
	sorted_dict = sorted(dict_shopping_cart_products.items(), key=lambda x: x[1], reverse=True)[:4]
	end_result = [] # will contain the top 4 products, without the dictionary values

	# small loop to put the products in final variable
	for product in sorted_dict:
		end_result.append(product[0])

	return(end_result)
