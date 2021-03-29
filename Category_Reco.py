
import psycopg2

#connect to the db
con = psycopg2.connect('host=localhost dbname=hu_webshop user=postgres password=123')

#cursor
cur = con.cursor()




def get_matching_prod():
    '''Function that receives information from Webshop
    This information contains  'Category' ,  and ' Sub-category ' when available.
    If there is a sub-category, get top 4 popular products with that  sub-category
    If there is no sub-category, but there is a category, get top 4 popular products with that category
    If there is no sub-category, and no category, fall back to fall_back()
    '''
    # temp vars used while front-end connection is not fully set up yet
    sub_category = []
    category = []
    # variable list that gets filled with recommendable products
    matching_products = []
    if sub_category != None:
        matching_products = cur.execute("select  product._id from product inner join populairste_prod on product._id = populairste_prod.productid where sub_category = '%s' LIMIT 5;",sub_category)
        return matching_products
    elif category != None:
        matching_products = cur.execute("select  product._id from product inner join populairste_prod on product._id = populairste_prod.productid where category = '%s' LIMIT 5;",category)
    else:
        fall_back()


def fall_back():
    '''This function gets called from get_matchin_prod
    This function only gets called when there is no category or sub-category to work with
    As the name suggests , This is a fallback function'''