#commente psycopg2 because im getting error whle in the train
#import psycopg2

#connect to the db
#con = psycopg2.connect('host=localhost dbname=hu_webshop user=postgres password=123')

#cursor
#cur = con.cursor()

def get_matching_prod(category,sub_category):
    '''Function that receives information from Webshop
    This information contains  'Category' ,  and ' Sub-category ' when available.
    If there is a sub-category, return  4 popular products with that  sub-category
    If there is 10 or less products with matching sub-category, try using category instead
    If there is no sub-category, but there is a category, return  4 popular products with that category
    If there is 10 or less products with matching category, go to fall_back()
    If there is no sub-category, and no category, fall back to fall_back()
    '''
    # temp vars used while front-end connection is not fully set up yet
    sub_category = []
    category = []
    # variable list that gets filled with recommendable products
    matching_products = []



    if sub_category != None:
        cur.execute("select  product._id from product inner join populairste_prod on product._id = populairste_prod.productid where sub_category = '%s';",sub_category)
        matching_products = cur.fetchall()
        if len(matching_products) > 10:
            cur.execute("select  product._id from product inner join populairste_prod on product._id = populairste_prod.productid where sub_category = '%s' LIMIT 4 ;",sub_category)
            matching_products = cur.fetchall()
            return matching_products
        else:
            fall_back()
    if category != None:
        cur.execute("select  product._id from product inner join populairste_prod on product._id = populairste_prod.productid where category = '%s';",category)
        matching_products = cur.fetchall()
        if len(matching_products) > 10:
            cur.execute("select  product._id from product inner join populairste_prod on product._id = populairste_prod.productid where category = '%s' LIMIT 4;",category)
            matching_products = cur.fetchall()
            return matching_products
        else:
            fall_back()
    else:
        fall_back()


def fall_back():
    '''This function gets called from get_matchin_prod
    This function only gets called when there is no category or sub-category to work with
    As the name suggests , This is a fallback function
    This function will show 4 recommendations
    These 4 recommendations are selected from the top 1500 products
    These top 1500 products have atleast 100 sales, which we deem is enough to base a recommendations on'''
    cur.execute("SELECT productid FROM populairste_prod WHERE rank < 1500 ORDER BY random() LIMIT 4")
    matching_products = cur.fetchall()
    return matching_products


matching_products = [('x',),('y',),('z',),('w',)]
def formatting_fix(matching_products):
    '''this function is made to change the formatting of the product ID's given by the cur.execute in get_matching_prod
    The original formatting after performing the execute =   [('x',),('y',),('z',),('w',)]
    We need this to change to: [ 'x', 'y', 'z', 'w' ]
    We need this to happen because of the way huw_reccommend uses date

    '''

    nieuwelijst=[]a
    for tjoeple in matching_products:
        nieuwelijst.append(str(tjoeple[0]))
    matching_products = nieuwelijst
    return matching_products
print(formatting_fix(matching_products))