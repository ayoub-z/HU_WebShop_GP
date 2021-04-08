import sys

def get_matching_prod(category, sub_category, cur, con):

    '''Function that receives information from Webshop
    This information contains  'Category' ,  and ' Sub-category ' when available.
    If there is a sub-category, return  4 popular products with that  sub-category
    If there is 10 or less products with matching sub-category, try using category instead
    If there is no sub-category, but there is a category, return  4 popular products with that category
    If there is 10 or less products with matching category, go to fall_back()
    If there is no sub-category, and no category, fall back to fall_back()
    '''

    # variable list that gets filled with recommendable products
    matching_products = []


    if sub_category != None:
        sub_category =  encodecategory(sub_category)
        try:
            cur.execute("select product._id from product inner join populairste_prod on product._id = populairste_prod.productid where sub_category = %s;",(sub_category,))
            matching_products = cur.fetchall()
        except InFailedTransaction as e:
            print(f'Error when fetching all items with X sub_category{e}', file=sys.stderr)
            con.rollback()
        if len(matching_products) > 10:
            cur.execute("select  product._id from product inner join populairste_prod on product._id = populairste_prod.productid where sub_category = %s LIMIT 4 ;",(sub_category,))
            matching_products = cur.fetchall()
            matching_products = formatting_fix(matching_products)
            return matching_products
    if category != None:
        category = encodecategory(category)
        try:
            cur.execute("select  product._id from product inner join populairste_prod on product._id = populairste_prod.productid where category = %s;",(category,))
            matching_products = cur.fetchall()
        except Exception as e:
            print(f'Error when fetching all items with X category{e}', file=sys.stderr)
            con.rollback()
        if len(matching_products) > 10:
            cur.execute("select  product._id from product inner join populairste_prod on product._id = populairste_prod.productid where category = %s LIMIT 4;",(category,))
            matching_products = cur.fetchall()
            matching_products = formatting_fix(matching_products)
            return matching_products
        else:
            return fall_back(cur)
    else:
        return fall_back(cur)

def fall_back(cur):
    '''This function gets called from get_matchin_prod
    This function only gets called when there is no category or sub-category to work with
    As the name suggests , This is a fallback function
    This function will show 4 recommendations
    These 4 recommendations are selected from the top 1500 products
    These top 1500 products have atleast 100 sales, which we deem is enough to base a recommendations on'''
    cur.execute("SELECT productid FROM populairste_prod WHERE rank < 1500 ORDER BY random() LIMIT 4")
    matching_products = cur.fetchall()
    matching_products = formatting_fix(matching_products)
    return matching_products

def formatting_fix(matching_products):
    '''this function is made to change the formatting of the product ID's given by the cur.execute in get_matching_prod
    The original formatting after performing the execute =   [('x',),('y',),('z',),('w',)]
    We need this to change to: [ 'x', 'y', 'z', 'w' ]
    We need this to happen because of the way huw_recommend uses data
    '''

    nieuwelijst=[]
    for tjoeple in matching_products:
        nieuwelijst.append(str(tjoeple[0]))
    matching_products = nieuwelijst
    return matching_products

def encodecategory(c):
        """ This helper function encodes any category name into a URL-friendly
        string, making sensible and human-readable substitutions. """
        c = c.capitalize()
        c = c.replace("_"," ")
        c = c.replace(".",",")
        c = c.replace("~","'")
        c = c.replace("-en-","&")
        c = c.replace("-ee-","ë")
        c = c.replace("-is-","=")
        c = c.replace("-procent-","%")
        return c