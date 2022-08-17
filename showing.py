import requests, os
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

import certifi
client = MongoClient(os.environ.get("MONGO"),tlsCAFile=certifi.where())
db = client.Sorting_Hat_Dev

url = 'https://movie.naver.com/movie/running/current.naver'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, li들을 불러오기
movies = soup.select('#content > div.article > div > div.lst_wrap > ul > li')

# db.movies.drop() # DB movie 컬렉션 삭제

# movies (li들) 의 반복문을 돌리기
for movie in movies:
    c_id = re.search(r'(?<=code\=)(.*?)$', movie.select_one('dl > dt > a')['href']).group() # 영화별 고유 ID값
    c_title = movie.select_one('dl > dt > a').text  # 영화제목
    c_img = movie.select_one('div > a > img')['src']  # 영화 이미지 링크

    # 영화 등급 가져오기
    # 등급 리스트
    # 전체 관람가
    # 12세 관람가
    # 15세 관람가
    # 청소년 관람불가
    # 청소년 유해물
    # 미정
    try:
        c_age = movie.select_one('dl > dt > span').text #
    except Exception as e:
        c_age = "미정"

    # 장르 가져오기 ['코미디', '드라마'] 형식
    c_genre = []
    c_genre_all = movie.select('dl > dd:nth-child(3) > dl > dd:nth-child(2) > span.link_txt > a')
    for c_genre_one in c_genre_all:
        c_genre.append(c_genre_one.text)

    c_n_star = movie.select_one('dl > dd.star > dl > dd:nth-child(2) > div > a > span.num').text  # 유저 평점
    try:
        c_r_star = movie.select_one('dl > dd.star > dl > dd:nth-child(4) > div > a > span.num').text  # 기자 평론가 평점
    except Exception as e:
        c_r_star = '0.00'
    c_release = re.search(r'\d{3,4}.*.봉', movie.select_one('dl > dd:nth-child(3) > dl > dd:nth-child(2)').text).group() # 개봉일

    doc = {
        'id' : c_id,
        'title': c_title,
        'image': c_img,
        'age' : c_age,
        'genre' : c_genre,
        'user_star': c_n_star,
        'reviewer_star': c_r_star,
        'release': c_release
    }
    db.movies.update_one(
        {'_id': doc['id']},
        {
            "$setOnInsert": {
                '_id': doc['id'],
                'title': doc['title'],
                'image': doc['image'],
                'age': doc['age'],
                'genre': doc['genre'],
                'user_star': doc['user_star'],
                'reviewer_star': doc['reviewer_star'],
                'release': doc['release'],
            }
        },
        upsert=True
    )

    # 또 다른 중복체크 방법
    # if db.movies.find_one(doc):
    #     continue
    # db.movies.insert_one(doc) # DB 최신데이타 등록
