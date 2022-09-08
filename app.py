import certifi
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime
from pymongo import MongoClient

import crawling

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.amhacid.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where())
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
            print('1번조건')
            continue
        elif movie['age'] == '15세 관람가' and rate_receive < 2:
            print('2번조건')
            continue
        elif movie['age'] == '12세 관람가' and rate_receive < 1:
            print('3번조건')
            continue
        else:
            for m_genre in movie['genre']:
                if genre_receive.count(m_genre) >= 1:
                    print(movie['title'])
                    return render_template('result.html', r_title=movie['title'], r_image=movie['image'])
    return render_template('noresult.html')


@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


@app.route('/showing')
def showing():
    return render_template('showing.html')


@app.route('/update', methods=["GET"])
def showing_get():
    movies_list = list(db.movies.find({}, {}))
    return jsonify({'movies': movies_list})


@app.route('/comment/get', methods=["GET"])
def comments_get():
    print(request.args.get('m_id'))
    comments_list = list(db.comments.find({'m_id': request.args.get('m_id')}, {'_id': False}).sort('time', -1))
    print(comments_list)
    return jsonify({'comments': comments_list})


@app.route('/comment/add', methods=["POST"])
def comments_add():
    result = request.form
    comment_time = datetime.now()
    db.comments.insert_one(
        {
            'm_id': result.get('movie_id'),
            'button': result.get('sel_btn'),
            'user': result.get('u_name'),
            'comment': result.get('comment'),
            'time': comment_time,
        }
    )
    return redirect(url_for(result.get('url')))


@app.route('/update_post', methods=["GET"])
def sca_get():
    id = request.args.get('id')
    movie = list(db.movies.find({'_id': id}, {}))
    movie[0]['video_url'] = crawling.get_video(id, movie[0]['image'])
    return jsonify({'movies': movie})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
