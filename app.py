from flask import Flask, render_template
from pymongo import MongoClient
app = Flask(__name__)

import certifi, requests
client = MongoClient('mongodb+srv://Sorting_Hat_Read:Sorting_Hat@cluster0.amhacid.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.Sorting_Hat_Dev

# movies_list = list(db.movies.find({}, {'_id': False}))
# print(movies_list)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/schedule')
def scadule():
    return render_template('schedule.html')

@app.route('/showing')
def showing():
    return render_template('showing.html')

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)