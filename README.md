# 항해99 9기 4조 ToyProject - Sorting Hat
> 현재 상영중인 영화중 취향에 맞는 영화를 추천해드립니다!

https://sorting_hat.pyuri.dev/

## 1. 팀원소개 및 담당 페이지
| 이름 | 담당 | 깃허브ID |
|---|:---:|---:|
| `김재명` | 영화 세부내용 modal 페이지 | [@JMKiim](https://github.com/JMKiim) | 
| `김상범` | 상영예정작 페이지, DB관리 | [@Puri12](https://github.com/Puri12) | 
| `황대연` | 현재상영작 페이지 | [@dyhwang](https://github.com/dyhwang)|
| `김민주` | 영화추천 페이지 | [@roses16-dev](https://github.com/roses16-dev) |
| `홍마로` | 영화추천 페이지 | [@hongmaro](https://github.com/hongmaro) |

## 2. 기획
#### 페이지 설명
### - 영화추천 페이지
![image](https://user-images.githubusercontent.com/5901912/189131485-3b1e424f-2966-4fdb-8a90-f81f5283a663.png)
![image](https://user-images.githubusercontent.com/5901912/189131556-42c10978-941f-4084-9378-f373727bd6d2.png)
![image](https://user-images.githubusercontent.com/5901912/189131622-8a776e9b-b568-4ab8-8b5d-3e83bfa0ef6f.png)
> 사용자의 나이 및 선호 장르를 기반하여 현재 상영중인 영화 추천

### - 현재상영작 페이지, 상영예정작 페이지
![image](https://user-images.githubusercontent.com/5901912/189131712-0b577e43-89fc-485c-bf4f-f0d1b366ac0e.png)
![image](https://user-images.githubusercontent.com/5901912/189131774-22768814-49b5-4a0c-9fa9-fd96ba25f0d1.png)
> 현재 상영중, 상영예정 영화 크롤링하여 표시 modal창을 이용하여 세부정보와 comment작성

### 📁 [figma 기획 페이지](https://www.figma.com/file/vJUYcXXqeRVoysYiRy8zMR/1st-toyproject?node-id=0%3A1) - [@roses16-dev](https://github.com/roses16-dev)

## 3. DB
### - movies
![image](https://user-images.githubusercontent.com/5901912/189132236-dd3ae8bf-fc6f-4613-a319-3dc7d6993e78.png)
### - comments
![image](https://user-images.githubusercontent.com/5901912/189132460-979dbc78-c2cb-4cf7-ac4c-19d330a0a598.png)

[movies DB 업데이트 python](showing.py) -> git actions를 이용하여 매일 새벽 5시 업데이트

[크롤링 함수 python](crawling.py)

## 4. Git Actions
1. [movies DB 매일 새벽 5시 업데이트](.github/workflows/showing_update.yml)
2. [pull request 시 서버에 페이지 자동 업로드](.github/workflows/update_server.yml)

#### DB 업데이트 상태
[![상영작 불러오기](https://github.com/HANGHAE99-Group-04-Study/Sorting_Hat/actions/workflows/showing_update.yml/badge.svg)](https://github.com/HANGHAE99-Group-04-Study/Sorting_Hat/actions/workflows/showing_update.yml)

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FHANGHAE99-Group-04-Study%2FSorting_Hat&count_bg=%23D127C4&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
