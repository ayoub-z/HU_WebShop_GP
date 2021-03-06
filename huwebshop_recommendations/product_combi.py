import sys
from score_filter import *

def product_combi(cartproducts, place, cur):
	'''Function returns the best 4 products that combine with the given product_id from shopping cart'''
	cartproducts = cartproducts.replace("'","")
	cartproducts = cartproducts.replace(" ","")
	cartproducts = cartproducts.strip("[]").split(",")
	cartproduct_id = cartproducts[place]	

	
	# sql query retrieves all 4 products that are a good combination with this product_id from table "product_combination"
	cur.execute("SELECT * FROM product_combination WHERE product_ID = %s", (str(cartproduct_id),))
	productlist = cur.fetchall()
	# checks that the count of how often the last product is bought is at least 5 or higher
	try:
		if productlist[0][5] >= 15:
			prodids = productlist[0][1:5]
			return prodids
	except IndexError as e:
		print(e, file=sys.stderr)
		return None

def product_combi_engine(cartproducts, lengthcart, place, cur):
	'''This function makes use of the function "product_combi" so that if there isn't a recommendation found for the last product,
	it tries to find a recommendation for the next product after it in the shoppingcart'''
	if product_combi(cartproducts, -1, cur) != None:
		return product_combi(cartproducts, -1, cur)
	elif lengthcart >= 2:
		for i in range(2, lengthcart+1):
			if product_combi(cartproducts, -i, cur) != None:
				return product_combi(cartproducts, -i, cur)
			else:
				continue
	else:
		return None

