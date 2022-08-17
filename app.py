from flask import Flask, render_template, jsonify
from pymongo import MongoClient
app = Flask(__name__)

import certifi, requests, os
client = MongoClient(os.environ.get("MONGO"),tlsCAFile=certifi.where())
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

@app.route('/showing/update', methods=["GET"])
def showing_get():
    movies_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies':movies_list})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)