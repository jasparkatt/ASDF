from app import app
from flask import render_template
import psycopg2
from app.settings import *

con = psycopg2.connect(database=PG_NAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
cursor = con.cursor()



# route for data entry to postgresql 'fishing' db tables
@app.route('/all_spots', methods=['POST', 'GET'])
def dataPage():
    cursor.execute("select id, stream, county, species from all_spots order by county asc")
    results = cursor.fetchall()
    data = {'center': [],'title': 'All Spots, All Species'}
    return render_template('public/data_all.html', data=data, results=results)


@app.route('/fav_cnty', methods=['POST','GET'])
def favcounty():
    cursor.execute("select * from visited_county where visited_county.total > 0;")
    results = cursor.fetchall()
    data = {'center': [],'title': 'Most Visited Counties'}
    return render_template('public/data_fav.html', data=data, results=results)  


@app.route('/fav_wtrshd', methods=['POST','GET'])
def fav_wtrshd():
    cursor.execute("select * from fav_wtrshd where fav_wtrshd.total > 0;")  
    results = cursor.fetchall()
    data = {'center': [],'title': 'Most Visited Watersheds'}
    return render_template('public/data_fav.html', data=data, results=results )