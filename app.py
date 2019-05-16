
# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo 
import mission_to_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

#------------------------------------------------------------------------------------#
# Local MongoDB connection #
#------------------------------------------------------------------------------------#
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
## create / Use database
db = client.mars_db
## create/use collection. 
coll = db.mars_data_coll

#------------------------------------------------------------------------------------#
## create route that renders index.html template and finds documents from mongo
# mars_db is the database; mars_data is the collection

@app.route("/")
def index():
    # Get the data from mongodb.
    mars_mission_data = coll.find_one()

    # return template and data
    return render_template("index.html", mars_mission_data=mars_mission_data)

from mission_to_mars import mars_scrape
#import python function from mars_scraping.py
# Route that will trigger scrape function.
@app.route("/scrape")
def scrape():
    # Run scrape function.
    mars_mission_data = mars_scrape()
    #print (f'in scrape function. will take a few min to  execute  - {type(mars_mission_data)}')
    #print (f'printing {mars_mission_data}')  

    # Insert mars_mission_data into database
    coll.update({"id": 1}, {"$set": mars_mission_data}, upsert = True)

    # Redirect back to home page
    #return redirect("/", code=302)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

