import psycopg2
import random
from db_connection import *
from similar_p_finder import *

def product_finder_query(product_id):
	'''
	Function finds the top 4 product_ids in table "product_order" that have been bought together
	with the given product_id in the same shopping cart the most as the given product_id 
	'''

	#sql query finds top 4 product_ids in the table "product_order" that have been bought the most with the given product_id
	cur.execute(
		"SELECT product_id,count(*) FROM product_order WHERE orderorderid in (SELECT orderorderid from product_order where product_id = %s)\
		 GROUP BY product_id ORDER BY COUNT(*) DESC",((product_id),))
	cart_products = cur.fetchall()[1:5]
	return(cart_products)

def shopping_cart_products(product_id):
	'''
	Function takes a product_id as input and goes through all shopping carts that contain
	this product_id. It then retrieves all other product_ids that are also in the same shopping cart
	besides this product_id. It then returns the 4 products_ids that have been the most commonly found.
	'''

	product_id = str(product_id)
	
	# function that returns 4 similar products
	similar_products = similarity_score(str(product_id))

	# holds all products that have been bought together with this product 
	cart_products = dict(product_finder_query(product_id))
	cart_products1 = dict(product_finder_query(similar_products[0][0]))
	cart_products2 = dict(product_finder_query(similar_products[1][0]))
	cart_products3 = dict(product_finder_query(similar_products[2][0]))
	cart_products4 = dict(product_finder_query(similar_products[3][0]))

	all_cart_products = cart_products | cart_products1 | cart_products2 | cart_products3 | cart_products4
	sorted_dict_cart_products = sorted(all_cart_products.items(), key=lambda x: x[1], reverse=True)[:4]

	# print(f"Top 4: {top4_products}")
	
	if len(sorted_dict_cart_products) == 4:
		end_result = []  # will contain product_id, the top 4 products, and count of lowest value from 4th product
		end_result.append(product_id)

		# small loop to put the products in final variable
		for product in sorted_dict_cart_products:
			end_result.append(product[0])

		# adds count of amount of times the last/lowest product has been bought together 
		end_result.append(sorted_dict_cart_products[3][1]) 
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
		combination_products = (shopping_cart_products(str(product[0])))
		# checks if we have enough data and all 6 columns in the database can be filled with this product_id
		if len(combination_products) == 6:
			# sql insert query to fill database
			# "lowest_combi_count" stands for the count for the product that has been bought together the least
			cur.execute("INSERT INTO product_combination (product_id, combi_product1, combi_product2, combi_product3, combi_product4, \
						lowest_combi_count) VALUES (%s, %s, %s, %s, %s, %s)", combination_products)
			con.commit()
			insert_count += 1
		else:
			skip_counter += 1
		print(f"Try: {insert_count + skip_counter} out of 31263")
	print(
		f"{insert_count} inserts \n{skip_counter} products have been skipped because they haven't been bought together with enough other products")


product_combination_filler()