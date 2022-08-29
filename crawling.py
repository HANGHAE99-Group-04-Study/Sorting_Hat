import re
import certifi
import os
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# ---test----
client = MongoClient(os.environ.get("MONGO"), tlsCAFile=certifi.where())
# client = MongoClient('mongodb://root:5pDpJVmytF^2g6iQs6UpAXf^jrtn4mZsd!k@10.1.0.10:27017')
db = client.Sorting_Hat_Dev

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = 'https://movie.naver.com/movie/bi/mi/basic.naver?code='  # 영화 정보

# # ---- 제목 ----
# def get_title(id):
#     data = requests.get(url + id, headers=headers)
#     soup = BeautifulSoup(data.text, 'html.parser')
#     title = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)').text
#     # content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(2)
#     return title


# ---- 이미지 URL ----
def get_image(id):
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    try:
        image = soup.select_one('#content > div.article > div.mv_info_area > div.poster > a > img')['src']
    except TypeError:
        image = 'https://ssl.pstatic.net/static/movie/2012/06/dft_img203x290.png'
    return image


# ---- 장르 ----
# return 값 예제: ['미스터리', '공포']
def get_genre(id):
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    genre_all = soup.select('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a')
    genre = []
    for genre_one in genre_all:
        genre.append(genre_one.text)
    return genre


# ---- 유저 평점 ----
# return 값 예제: 8.56
def get_user_star(id):
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    user_star_all = soup.select('#pointNetizenPersentBasic > em')
    user_star = []
    for user_star_one in user_star_all:
        user_star.append(user_star_one.text)
    return ''.join(user_star)


# ----  평점 ----
# return 값 예제: 8.56
def get_reviewer_star(id):
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    reviewer_star_all = soup.select('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div:nth-child(2) > div > a > div > em')
    reviewer_star = []
    for reviewer_star_one in reviewer_star_all:
        reviewer_star.append(reviewer_star_one.text)
    return ''.join(reviewer_star)


# ---- 국가 ----
# return 값 예제: 한국
def get_nation(id):
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    try:
        nation = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(2) > a').text
    except AttributeError:
        nation = ''
    return nation


# ---- 러닝타임 ----
# return 값 예제: 123분
def get_time(id):
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    try:
        time = re.search(r'\d.*.분',soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)').text)
        if time is None:
            time = ''
        else:
            time = time.group()
    except AttributeError:
        time = ''
    return time


# ---- 개봉일 ----
# return 값 예제
# 2022.08.18 개봉
# 2022.08 개봉
# 2022 개봉
def get_day(id):
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    days = soup.select('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span')
    day_list = []
    for day in days:
        day_list.append(str(day))
    day_str = ''.join(day_list)
    try:
        result = re.search(r'(?<=open=)([0-9]{8})(?=")', day_str).group()
        result = result[:4] + "." + result[4:6] + "." + result[6:]
        result = result.replace('.00', '') + " 개봉"
    except AttributeError:
        result = ''
    return result


# ---- 감독 ----
# return 값 예제: 소피 하이드
def get_director(id):
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    try:
        director = soup.select_one(
            '#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a').text
    except AttributeError:
        director = ''
    return director


# ---- 배우 ----
# return 값 예제: ['나문희(금분), 최우성(지웅)']
def get_actor(id):
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    actor = []
    if soup.find(class_='step3') is None:
        return ''
    else:
        actor_all = soup.select('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(6) > p')
        for actor_one in actor_all:
            actor.append(actor_one.text)
    return actor


# ---- 줄거리 ----
# return 값 예제: 8.56
def get_tx(id):
    print(url + id)
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    try:
        text = soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div > p').text
        # tx = re.sub(r"^\s+|\s+$", "", tx)
    except AttributeError:
        text = '내용없음'
    return text


# ---- 등급 ----
# return 값 예제
# 청소년 관람불가
# 15세 관람가
# 12세 관람가
# 전체 관람가
# 미정
def get_grade(id):
    data = requests.get(url + id, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    if soup.find(class_='step4') is None:
        return '미정'
    else:
        try:
            grade = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a').text
            if grade == 'NR':
                grade = '미정'
        except AttributeError:
            grade = '미정'
    return grade


# ---- 비디오 URL ----
def get_video(id, img):
    video_url = 'https://movie.naver.com/movie/bi/mi/media.naver?code='
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

