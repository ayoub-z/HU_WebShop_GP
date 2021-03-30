import psycopg2
import random

#connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=12345')

#cursor
cur = con.cursor()



def shopping_cart_products(product_id):
	'''
	Function takes a product_id as input and goes through all shopping carts that contain
	this product_id. It then retrieves all other product_ids that are also in the same shopping cart
	besides this product_id. It then returns the 4 products_ids that have been the most commonly found.
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
	# checks if there are at least 4 products bought together with the given product_id
	if len(sorted_dict) == 4:
		end_result = [] # will contain the top 4 products, without the dictionary values
		end_result.append(product_id)

		# small loop to put the products in final variable
		for product in sorted_dict:
			end_result.append(product[0])

		# adds amount of times the last/lowest product has been bought together with the given product
		end_result.append(sorted_dict[3][1])
		return(end_result)
	else:
		return('0')



def product_combination_filler():
	'''
	Function creates and fills table "product_combination"
	'''
	
	# sql query that creates product_combination table
	cur.execute("CREATE TABLE IF NOT EXISTS product_combination (product_id VARCHAR (40) NOT NULL, combi_product_1 varchar(255) NOT NULL, combi_product_2 varchar(255) NOT NULL, \
			combi_product_3 varchar(255) NOT NULL, combi_product_4 varchar(255) NOT NULL, lowest_combi_count int4 NOT NULL, PRIMARY KEY (product_id));")

	# sql query to receive all product_id's from table product
	cur.execute("SELECT _id FROM product")
	all_products = cur.fetchall()
	
	insert_count = 0
	skip_counter = 0
	for product in all_products:
		# checks if there are at least 4 other products bought together with this product
		if len(shopping_cart_products(product[0])) == 6:
			# sql insert query to fill database
			# "lowest_combi_count" means product that has been bought together with given product_id the lowest amount of times out of top 4 results
			cur.execute("INSERT INTO product_combination (product_id, combi_product_1, combi_product_2, combi_product_3, combi_product_4, lowest_combi_count) \
			VALUES (%s, %s, %s, %s, %s, %s)", shopping_cart_products(product[0]))
			insert_count += 1
			print(f"Inserted: {insert_count} out of 11598")
		else:
			skip_counter += 1
			pass
	
	print(f"{insert_count} inserts \n{skip_counter} products have been skipped because they haven't been bought together with enough other products")

product_combination_filler()

con.commit()

cur.close()
con.close()

