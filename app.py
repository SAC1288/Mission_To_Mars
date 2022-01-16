from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from scrape import scrape_all, facts
from config import DB


app = Flask(__name__)



app.config["MONGO_URI"] = DB
mongo = PyMongo(app).db
# mongo.todos.insert_one({"tite":"hello"})
# mongo.mars.insert_one({"news_title":"hello", "news_paragraph":"hi"})

# print(facts())
# print("ge")
# print(bar)
# db = mongo.admin
# res = db.command("serverStatus")
# print(res)
# mars_data = scrape_all()
# mars = mongo.db.mars.find_one()
# print("hello",mars)
@app.route("/")
def index():

    mars = mongo.mars.find_one()
    # print(mars.hemispheres)
    return render_template("foo.html", mars=mars)
    # return render_template("./templates/index.html", mars=mars)

@app.route("/scrape")
def scrape():
    try:
        mars = mongo.mars
        mars_data = scrape_all()
        # print(mars_data)
        mars.update_one({}, {"$set":mars_data}, upsert=True)
        # print("success")
        return redirect('/', code=302)
    except:
        print("error")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) 

