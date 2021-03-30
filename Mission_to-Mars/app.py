from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo Connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

#Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars_data = mongo.db.mars_db.find_one()
    return render_template("index.html", mars_data=mars_data)


#Route to scrape function
@app.route("/scrape")
def scrape():
    mars_db = mongo.db.mars_db
    mars_data = scrape_mars.scrape()
    mars_db.update({}, mars_data , upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)