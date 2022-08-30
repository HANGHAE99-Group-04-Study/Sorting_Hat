import re
import certifi
import os
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient(os.environ.get("MONGO"), tlsCAFile=certifi.where())
db = client.Sorting_Hat_Dev

db.movies.update_many({}, {"$set": {'showing': 0}})  # DB에 있는 전체 영화 상영여부 False로 변환

# ------------URL 변수-------------------
current_url = 'https://movie.naver.com/movie/running/current.naver'  # 현재 상영작
premovie_url = 'https://movie.naver.com/movie/running/premovie.naver'  # 상영 예정작

# ------------URL 가져오는 함수-------------

def get_url(url, tag):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    # select를 이용해서, li들을 불러오기
    movies = soup.select('#content > div.article > div > div.lst_wrap > ul > li')

    # db.movies.drop() # DB movie 컬렉션 삭제

    # movies (li들) 의 반복문을 돌리기
    for movie in movies:
        c_id = re.search(r'(?<=code=)(.*?)$', movie.select_one('dl > dt > a')['href']).group()  # 영화별 고유 ID값
        c_title = movie.select_one('dl > dt > a').text  # 영화제목
        c_showing = tag


        doc = {
            'id': c_id,
            'title': c_title,
            'showing': c_showing,
        }


        db.movies.update_one(
            {'_id': doc['id']},
            {
                "$setOnInsert": {
                    '_id': doc['id'],
                    'title': doc['title'],
                    'showing': doc['showing']
                },
            },
            upsert=True
        )


        db.movies.update_one(
            {'_id': doc['id']},
            {
                "$set": {
                    'title': doc['title'],
                    'showing': doc['showing']
                },
            }
        )


get_url(current_url, 1)
get_url(premovie_url, 2)
