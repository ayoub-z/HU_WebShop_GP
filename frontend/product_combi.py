import psycopg2
from database_setup.db_connection import cur
import sys

def product_combi(lastcartproductid, place):
	'''
	Function returns the best 4 products that combine with the given product_id from shopping cart 
	'''
	lastcartproductid = lastcartproductid.replace("'","")
	lastcartproductid = lastcartproductid.replace(" ","")
	lastcartproductid = lastcartproductid.strip("[]").split(",")
	lastcartproductid = lastcartproductid[place]	
	# sql query retrieves all 4 products that are a good combination with this product_id from table "product_combination"
	cur.execute("SELECT * FROM product_combination WHERE product_ID = %s", (str(lastcartproductid),))
	productlist = cur.fetchall()
	# print(productlist, file=sys.stderr)
	# checks that the count of how often the last product is bought is at least 5 or higher
	try:
		if productlist[0][5] >= 5:
			prodids = productlist[0][1:5]
			return prodids
	except Exception as e:
		print(e, file=sys.stderr)
		return None

def product_combi_engine(lastcartproductid, lengthcart, place):
	'''
	This function makes use of the function "product_combi" so that if there isn't a recommendation found for the last product,
	it tries to find a recommendation for the next product after it in the shoppingcart
	'''
	if product_combi(lastcartproductid, -1) != None:
		return product_combi(lastcartproductid, -1)
	elif lengthcart >= 2:
		for i in range(2, lengthcart+1):
			if product_combi(lastcartproductid, -i) != None:
				return product_combi(lastcartproductid, -i)
			else:
				continue
	else:
		return None