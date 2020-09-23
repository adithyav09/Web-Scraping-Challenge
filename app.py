from flask import Flask, render_template, redirect 
import pymongo
from scrape_mars import scrape

app = Flask(__name__)

client = pymongo.MongoClient()

db = client.mars_app

mars_data_col = db.mars_data

# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = pymongo(app)

@app.route('/')
def index():
    mars = mars_data_col.find_one()
    return render_template('index.html', mars=list(mars_data_col.find())[-1])

@app.route('/scrape')
def scrape_Mars():
    mars = mars_data_col
    data = scrape()
    mars.insert_one(
        data
    )

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
