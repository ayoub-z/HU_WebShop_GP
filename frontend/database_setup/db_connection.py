
import psycopg2

#connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=Levidov123')
cur = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=Levidov123').cursor()