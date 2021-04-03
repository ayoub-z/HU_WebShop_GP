import psycopg2
import random
from db_connection import *

def product_finder_query(product_id):
	'''
	Function finds other product_ids in table "product_order" that have been bought together
	in the same shopping carts as the given product_id
	'''

	#sql query that finds all product_ids in the table "product_order" that are in the same "orderorderid" as the given product_id
	cur.execute(
		"SELECT product_id FROM product_order WHERE orderorderid in (SELECT orderorderid from product_order where product_id = %s)",(str(product_id),))
	cart_products = cur.fetchall()

	return(cart_products)

def products_dict(product_id, shopping_cart_products):
	'''
	Function puts products in a dictionary, sorts them and picks the 4 products that have the highest value
	'''

	dict_shopping_cart_products = {}

	for product in shopping_cart_products:
		# add product to dictionary if it's not in it already and if product isn't the initial product_id
		if product[0] not in dict_shopping_cart_products and product[0] != product_id:
			dict_shopping_cart_products[product[0]] = 1
		# add +1 to value of this product if it's already in the dictionary
		if product[0] in dict_shopping_cart_products and product[0]:
			dict_shopping_cart_products[product[0]] += 1

	sorted_dict = sorted(dict_shopping_cart_products.items(), key=lambda x: x[1], reverse=True)	

	return(sorted_dict)

def shopping_cart_products(product_id):
	'''
	Function takes a product_id as input and goes through all shopping carts that contain
	this product_id. It then retrieves all other product_ids that are also in the same shopping cart
	besides this product_id. It then returns the 4 products_ids that have been the most commonly found.
	'''
	
	# sql query to find 4 similar products based on score_similary algorithm
	cur.execute("SELECT * FROM score_recommendation WHERE productid = %s", (str(product_id),))
	similar_products = cur.fetchall()[0]

	# holds all products that have been bought together with this product 
	cart_products = product_finder_query(similar_products[0])
	# dictionary, descending from products that have been bought the most with the given product_id, to least
	sorted_dict = products_dict(similar_products[0], cart_products)

	cart_products1 = product_finder_query(similar_products[1])
	sorted_dict1 = products_dict(similar_products[1], cart_products1)

	cart_products2 = product_finder_query(similar_products[2])
	sorted_dict2 = products_dict(similar_products[2], cart_products2)

	cart_products3 = product_finder_query(similar_products[3])
	sorted_dict3 = products_dict(similar_products[3], cart_products3)

	cart_products4 = product_finder_query(similar_products[4])
	sorted_dict4 = products_dict(similar_products[4], cart_products4)

	# merging all dictionaries
	dict_cart_products = dict(sorted_dict) | dict(sorted_dict1) | dict(sorted_dict2) | dict(sorted_dict3) | dict(sorted_dict4)
	# sorting dictionary and picking top 5. Reason it's 5 instead of 4, is since original product_id might also be in the dictionary
	sorted_dict_cart_products = sorted(dict_cart_products.items(), key=lambda x: x[1], reverse=True)[:5]
	
	if len(sorted_dict_cart_products) == 5:
		end_result = []  # will contain product_id, the top 4 products, and count of lowest value from 4th product
		end_result.append(product_id)

		# small loop to put the products in final variable
		for product in sorted_dict_cart_products:
			if product != product_id:
				end_result.append(product[0])
		
		# trimming away the 5th top product, so now it contains initial product, plus the top 4 products
		end_result = end_result[:5]

		# adds count of amount of times the last/lowest product has been bought together 
		end_result.append(sorted_dict_cart_products[4][1])
		return(end_result)
	else:
		return ('0')

def product_combination_filler():
	'''
	Function creates and fills table "product_combination" by making use of the 
	product_combination recommendation.
	'''

	# sql query that creates product_combination table
	cur.execute("CREATE TABLE IF NOT EXISTS product_combination (product_id VARCHAR (40) NOT NULL, combi_product1 varchar(255) NOT NULL,\
		 		combi_product2 varchar(255) NOT NULL, combi_product3 varchar(255) NOT NULL, combi_product4 varchar(255) NOT NULL, \
				lowest_combi_count int4 NOT NULL, PRIMARY KEY (product_id));")
	con.commit()

	# sql query to receive all product_id's from table product
	cur.execute("SELECT _id FROM product")
	all_products = cur.fetchall()

	insert_count = 0
	skip_counter = 0
	for product in all_products:
		# checks if we have enough data and all 6 columns in the database can be filled with this product_id
		if len(shopping_cart_products(product[0])) == 6:
			# sql insert query to fill database
			# "lowest_combi_count" stands for the count for the product that has been bought together the least
			cur.execute("INSERT INTO product_combination (product_id, combi_product1, combi_product2, combi_product3, combi_product4, \
						lowest_combi_count) VALUES (%s, %s, %s, %s, %s, %s)", shopping_cart_products(product[0]))
			con.commit()
			insert_count += 1
			print(f"Insert: {insert_count}")
		else:
			skip_counter += 1
			pass

	print(
		f"{insert_count} inserts \n{skip_counter} products have been skipped because they haven't been bought together with enough other products")

product_combination_filler()
