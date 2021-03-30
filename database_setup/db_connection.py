import psycopg2

#connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=12345')
cur = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=12345').cursor()