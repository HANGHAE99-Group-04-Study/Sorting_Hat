import requests
from bs4 import BeautifulSoup
import re

url = 'https://movie.naver.com/movie/running/current.naver'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, li들을 불러오기
movies = soup.select('#content > div.article > div > div.lst_wrap > ul > li')

# movies (li들) 의 반복문을 돌리기
for movie in movies:
    c_title = movie.select_one('dl > dt > a')  # 영화제목
    c_img = movie.select_one('div > a > img')['src']  # 영화 이미지 링크
    c_n_star = movie.select_one('dl > dd.star > dl > dd:nth-child(2) > div > a > span.num').text  # 유저 평점
    try:
        c_r_star = movie.select_one('dl > dd.star > dl > dd:nth-child(4) > div > a > span.num').text  # 기자 평론가 평점
    except Exception as e:
        c_r_star = '0.00'
    c_release = re.search(r'\d{3,4}.*.봉', movie.select_one('dl > dd:nth-child(3) > dl > dd:nth-child(2)').text).group() # 개봉일

    print(c_title.text, " ", c_img, " ", c_n_star, " ", c_r_star, " ", c_release)
