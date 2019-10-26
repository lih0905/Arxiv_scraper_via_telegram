# Arxiv.org 스크레이퍼

매일 아침 8시에 Arxiv의 Computation and Language 카테고리에 접속하여 전날 올라온 논문 리스트를 스크레이핑하여 텔레그램으로 정보를 송출 및 SQL에 업데이트하는 프로그램. 라즈베리파이를 써먹어보고자 만들어봄...

혹시나 이 프로그램을 쓰실 분이 계시다면, 텔레그램봇 주소와 본인 텔레그램 id 로 변경이 필요합니다. 또한 다른 카테고리의 논문 정보를 스크랩하고 싶으면 url과 full_url에서 cs.CL 부분을 원하는 카테고리로 변경하면 됩니다.

필요 패키지 :
* BeautifulSoup4
* requests
* python-telegram-bot
* pymysql

