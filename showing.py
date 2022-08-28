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

# ------------Video URL 가져오는 함수-------------
def get_video(id, img):
    video_url = 'https://movie.naver.com/movie/bi/mi/media.naver?code='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(video_url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    # select를 이용해서, li들을 불러오기
    try:
        video_url = "https://movie.naver.com" + soup.select_one(
            '#content > div.article > div.obj_section2.noline > div > div.ifr_module > div.ifr_trailer > div > ul > li:nth-child(1) > p.tx_video.ico > a')[
            'href']
        data = requests.get(video_url + id, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        video_url = "https://movie.naver.com" + re.search(r'.*.(?=&mid)',
                                                          soup.select_one('#videoPlayer')['src']).group()
    except Exception:
        video_url = img
    return video_url

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
        try:
            c_img = re.search(r'(.*?)(?=\?)', movie.select_one('div > a > img')['src']).group()  # 영화 이미지 링크
        except AttributeError:
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
            c_age = movie.select_one('dl > dt > span').text
        except AttributeError:
            c_age = "미정"

        # 장르 가져오기 ['코미디', '드라마'] 형식
        c_genre = []
        c_genre_all = movie.select('dl > dd:nth-child(3) > dl > dd:nth-child(2) > span.link_txt > a')
        for c_genre_one in c_genre_all:
            c_genre.append(c_genre_one.text)

        try:
            c_n_star = movie.select_one('dl > dd.star > dl > dd:nth-child(2) > div > a > span.num').text  # 유저 평점
        except AttributeError:
            c_n_star = '0.00'
        try:
            c_r_star = movie.select_one('dl > dd.star > dl > dd:nth-child(4) > div > a > span.num').text  # 기자 평론가 평점
        except AttributeError:
            c_r_star = '0.00'
        c_release = re.search(r'\d{3,4}.*.봉',
                              movie.select_one('dl > dd:nth-child(3) > dl > dd:nth-child(2)').text).group()  # 개봉일
        c_v_url = get_video(c_id, c_img)
        c_showing = tag

        movie_data = requests.get("https://movie.naver.com/movie/bi/mi/basic.naver?code=" + c_id, headers=headers)
        soup_detail = BeautifulSoup(movie_data.text, 'html.parser')
        # select를 이용해서, li들을 불러오기
        movie_details = soup_detail.select('#content > div.article')
        for movie_detail in movie_details:
            try:
                c_tx = movie_detail.select_one(
                    'div.section_group.section_group_frst > div:nth-child(1) > div > div > p').text
            except AttributeError:
                c_tx = "내용없음"
            doc = {
                'id': c_id,
                'title': c_title,
                'image': c_img,
                'age': c_age,
                'genre': c_genre,
                'user_star': c_n_star,
                'reviewer_star': c_r_star,
                'tx': c_tx,
                'video_url': c_v_url,
                'release': c_release,
                'showing': c_showing,
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
                        'tx': doc['tx'],
                        'video_url': doc['video_url'],
                        'release': doc['release'],
                        'showing': doc['showing']
                    },
                },
                upsert=True
            )
            print(doc)
            db.movies.update_one(
                {'_id': doc['id']},
                {
                    "$set": {
                        'showing': doc['showing'],
                        'user_star': doc['user_star'],
                        'tx': doc['tx'],
                        'reviewer_star': doc['reviewer_star']
                    },
                }
            )


get_url(current_url, 1)
get_url(premovie_url, 2)
