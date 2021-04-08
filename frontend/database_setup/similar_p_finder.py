import psycopg2
import itertools
from db_connection import *

def productfetcher(product_id):
	'''this function fetches all products except the productid in the function arguments'''
	cur = con.cursor()
	cur.execute("SELECT _id, category, selling_price, doelgroep, sub_category, sub_sub_category FROM product WHERE _id != %s", (product_id,))
	return cur.fetchall()

def startproductfetcher(product_id):
	'''this function fetches one specific product'''
	cur = con.cursor()
	cur.execute("SELECT _id, category, selling_price, doelgroep, sub_category, sub_sub_category FROM product WHERE _id = %s", (product_id,))
	return cur.fetchone()

def similarity_score(product_id):
	'''this function assigns similarity score based on category, selling price, doelgroep, sub_cat and sub_sub_cat
	it saves these scores in a dict and returns the top 4 products in that dict. 
	Per product, we look at ALL other products and score them'''
	similarity_score_dict = {}
	productlist = productfetcher(product_id)
	startproduct = startproductfetcher(product_id)

	#this allows us to easily adjust the weight of certain attributes. Higher number = higher weight
	categoryweight = 1
	priceweight = 0.2
	doelgroepweight = 1	
	sub_categoryweight = 1
	sub_sub_categoryweight = 1

	for product in productlist:
		if startproduct[3] == "Vrouwen" or startproduct[3] == "Mannen":
			if product[3] == startproduct[3]:
				#sub_sub_category
				similarity_score_dict[product[0]] = 0.1
				#category points
				if product[1] != None and product[1] == startproduct[1]:
					similarity_score_dict[product[0]] += categoryweight
				#price within 20% of start?
				if 110 > (100 * product[2]/startproduct[2]) > 90:
					similarity_score_dict[product[0]] += priceweight
				if product[4] != None and product[4] == startproduct[4]:
					similarity_score_dict[product[0]] += sub_categoryweight
				#sub_sub_category
				if product[5] != None and product[5] == startproduct[5]:
					similarity_score_dict[product[0]] += sub_sub_categoryweight
				continue
			else:
				continue
		#sub_sub_category
		similarity_score_dict[product[0]] = 0.1
		#category points
		if product[1] != None and product[1] == startproduct[1]:
			similarity_score_dict[product[0]] += categoryweight
		#price within 20% of start?
		if 110 > (100 * product[2]/startproduct[2]) > 90:
			similarity_score_dict[product[0]] += priceweight
		#doelgroep
		if product[3] != None and product[3] == startproduct[3]:
			similarity_score_dict[product[0]] += doelgroepweight
		if product[4] != None and product[4] == startproduct[4]:
			similarity_score_dict[product[0]] += sub_categoryweight
		#sub_sub_category
		if product[5] != None and product[5] == startproduct[5]:
			similarity_score_dict[product[0]] += sub_sub_categoryweight
	sorted_score_dict = sorted(similarity_score_dict.items(), key=lambda x: x[1], reverse=True)[:4]

	if sorted_score_dict[3][1] < 2:
		return[]
	else:
		return sorted_score_dict