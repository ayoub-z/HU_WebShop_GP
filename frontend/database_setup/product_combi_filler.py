from db_connection import *
from similar_p_finder import *
from decimal import *


def product_finder_query(product_id, cur):
	'''
	Function finds other product_ids in table "product_order" that have been bought together
	in the same shopping carts as the given product_id
	'''

	#sql query that finds all product_ids in the table "product_order" that are in the same "orderorderid" as the given product_id
	cur.execute(
		"SELECT product_id FROM product_order WHERE orderorderid in (SELECT orderorderid from product_order where product_id = %s)",(str(product_id),))
	cart_products = cur.fetchall()

	return(cart_products)

def products_dict(starter_productid, product_id, shopping_cart_products, cur):
	'''
	Function puts products in a dictionary, sorts them and picks the 4 products that have the highest value
	'''

	dict_shopping_cart_products = {}

	for product in shopping_cart_products:
		# add +1 to value of this product if it's already in the dictionary
		if product[0] in dict_shopping_cart_products:
			dict_shopping_cart_products[product[0]] += 1		
		# add product to dictionary if it's not in it already and if product isn't the initial product_id
		if product[0] not in dict_shopping_cart_products and product[0] != product_id and product[0] != starter_productid:
			dict_shopping_cart_products[product[0]] = 1

	sorted_dict = sorted(dict_shopping_cart_products.items(), key=lambda x: x[1], reverse=True)[:4]

	return(sorted_dict)

def lift_function(starter_productid, product_id, shopping_cart_products, cur):
	'''
	This function replaces the AMOUNT of times a product has been bought together with the main product,
	with the PERCENTAGE of how often it has been bought with the main product.
	'''
	# amount of times product has been bought
	cur.execute("SELECT COUNT(*) FROM product_order WHERE product_id = %s", (str(product_id),))
	purchase_amount = cur.fetchone()[0]

	dict_products = products_dict(starter_productid, product_id, shopping_cart_products, cur)
	list_products = [str(item) for t in dict_products for item in t]

	# same as Decimal('0.01')
	TWOPLACES = Decimal(10) ** -2

	# here we round each percentage to 2 decimals
	for p in range (1, len(list_products)+1, 2):
		lift_method = 100 / int(purchase_amount) * int(list_products[p])
		list_products[p] = float(Decimal(lift_method).quantize(TWOPLACES))

	# convert back to tuples in list
	final_products = []
	for p in range (0, len(list_products)-2, 2):
		final_products.append(list_products[p:p+2])
	return final_products

def shopping_cart_products(product_id, cur):
	'''
	Function takes a product_id as input and goes through all shopping carts that contain
	this product_id. It then retrieves all other product_ids that are also in the same shopping cart
	besides this product_id. It then returns the 4 products_ids that have been the most commonly found.
	'''
	# sql query to find 4 similar products based on score_similary algorithm
	similar_products = similarity_score(str(product_id), cur)

	# holds all products that have been bought together with this product 
	cart_products = product_finder_query(product_id, cur)
	# dictionary, descending from products that have been bought the most with the given product_id, to least
	sorted_dict = lift_function(product_id, product_id, cart_products, cur)

	if len(similar_products) == 4:
		cart_products1 = product_finder_query(similar_products[0][0], cur)
		sorted_dict1 = lift_function(product_id, similar_products[0][0], cart_products1, cur)

		cart_products2 = product_finder_query(similar_products[1][0], cur)
		sorted_dict2 = lift_function(product_id, similar_products[1][0], cart_products2, cur)

		cart_products3 = product_finder_query(similar_products[2][0], cur)
		sorted_dict3 = lift_function(product_id, similar_products[2][0], cart_products3, cur)

		cart_products4 = product_finder_query(similar_products[3][0], cur)
		sorted_dict4 = lift_function(product_id, similar_products[3][0], cart_products4, cur)

		# merging all dictionaries
		dict_cart_products = dict(sorted_dict) | dict(sorted_dict1) | dict(sorted_dict2) | dict(sorted_dict3) | dict(sorted_dict4)

	elif len(similar_products) == 3:
		cart_products1 = product_finder_query(similar_products[0][0], cur)
		sorted_dict1 = lift_function(product_id, similar_products[0][0], cart_products1, cur)

		cart_products2 = product_finder_query(similar_products[1][0], cur)
		sorted_dict2 = lift_function(product_id, similar_products[1][0], cart_products2, cur)

		cart_products3 = product_finder_query(similar_products[2][0], cur)
		sorted_dict3 = lift_function(product_id, similar_products[2][0], cart_products3, cur)

		# merging all dictionaries
		dict_cart_products = dict(sorted_dict) | dict(sorted_dict1) | dict(sorted_dict2) | dict(sorted_dict3) 


	elif len(similar_products) == 2:
		cart_products1 = product_finder_query(similar_products[0][0], cur)
		sorted_dict1 = lift_function(product_id, similar_products[0][0], cart_products1, cur)

		cart_products2 = product_finder_query(similar_products[1][0], cur)
		sorted_dict2 = lift_function(product_id, similar_products[1][0], cart_products2, cur)

		# merging all dictionaries
		dict_cart_products = dict(sorted_dict) | dict(sorted_dict1) | dict(sorted_dict2) 

	elif len(similar_products) == 1:
		cart_products1 = product_finder_query(similar_products[0][0], cur)
		sorted_dict1 = lift_function(product_id, similar_products[0][0], cart_products1, cur)

		# merging all dictionaries
		dict_cart_products = dict(sorted_dict) | dict(sorted_dict1) 

	else:
		dict_cart_products = dict(sorted_dict)

	# sorting dictionary and picking top 4.
	sorted_dict_cart_products = sorted(dict_cart_products.items(), key=lambda x: x[1], reverse=True)[:4]
	if len(sorted_dict_cart_products) == 4:
		avg_bought_amount = (sorted_dict_cart_products[0][1] + sorted_dict_cart_products[1][1] + sorted_dict_cart_products[2][1] + sorted_dict_cart_products[3][1]) / 4 

	if len(sorted_dict_cart_products) == 4:
		end_result = []  # will contain product_id, the top 4 products, and count of lowest value from 4th product
		end_result.append(product_id)

		# small loop to put the products in final variable
		for product in sorted_dict_cart_products:
			end_result.append(product[0])

		# adds count of amount of times the last/lowest product has been bought together 
		end_result.append(avg_bought_amount)
		return(end_result)
	else:
		return ('0')

def product_combination_filler(con, cur):
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
		combination_products = (shopping_cart_products(str(product[0]), cur))
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

product_combination_filler(con, cur)