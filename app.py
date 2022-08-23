from flask import Flask, render_template, jsonify, request
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

@app.route('/recommend/calc', methods=["POST"])
def recommend_calc():
    movies_list = list(db.movies.find({'showing': 1}, {'_id': False}).sort('reviewer_star', -1))
    rate_receive = int(request.form['give_rate'])
    genre_receive = request.form.getlist('give_genre[]')

    print(genre_receive, rate_receive)

    for movie in movies_list:
        print(movie)
        if movie['age'] == '청소년 관람불가' and rate_receive < 3:
            continue
        elif movie['age'] == '15세 관람가' and rate_receive < 2:
            continue
        elif movie['age'] == '12세 관람가' and rate_receive < 1:
            continue
        else:
            for m_genre in movie['genre']:
                if genre_receive.count(m_genre) >= 1:
                    print(movie['title'])
                    return render_template('result.html', r_title=movie['title'])
            return render_template('noresult.html')

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