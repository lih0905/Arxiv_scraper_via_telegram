# -*- coding: utf-8 -*-

"""
매일 아침 8시에 전날 arxiv.org에 올라온 Computation and Language 카테고리의
논문을 모두 스크랩하여 텔레그램으로 메세지를 보내주는 프로그램입니다.
"""

import requests
import telegram
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

# 텔레그램봇 설정 및 최초 페이지 설정
bot = telegram.Bot(token='970060618:AAFbYa2iflYVkwzmoDddsapDXTgJZ0xCKCE')
url='https://arxiv.org/list/cs.CL/recent'


def job_function():
    # 최근 논문이 올라오는 페이지를 불러옴
    html = requests.get(url)
    bs = BeautifulSoup(html.text, 'html.parser')

    # 처음엔 25개까지만 표시되도록 되어 있기 때문에, 최근 올라온 논문 갯수를 스크랩한 후
    # 모든 논문의 갯수만큼 표시되도록 페이지를 재로딩
    full_url = 'https://arxiv.org/list/cs.CL/pastweek?show='+((bs.find('small').findAll('a'))[-1].text)
    full_html = requests.get(full_url)
    bs = BeautifulSoup(full_html.text, 'html.parser')

    # 일자별 논문 리스트는 dl 태그로 분리되어 있으므로 가장 최근 dl을 불러오면 된다.
    today_data = bs.find('dl')

    # 논문의 정보(제목, 저자, 카테고리)는 dd 태그, 링크는 dt > a.Abstract 에 저장된다.
    info_list = today_data.findAll('dd')
    link_list = today_data.findAll('a', title='Abstract')
    link_results = ['https://arxiv.org'+link.attrs['href'] for link in link_list]

    results = []

    for data, link in zip(info_list, link_results):
        # 각 논문의 정보를 딕셔너리로 저장한다.
        paper_data = {}
        paper_data['title'] = data.find('div', class_='list-title mathjax').text.replace('Title: ','').strip('\n').replace('  ', ' ')
        paper_data['authors'] = data.find('div', class_='list-authors').text.replace('Authors:','').replace('\n','')
        paper_data['category'] = data.find('div', class_='list-subjects').text.replace('Subjects: ','').replace('\n','')
        paper_data['link'] = link
        results.append(paper_data)

    # 오늘 올라온 논문 갯수를 먼저 알려준 후 각 논문의 정보를 차례대로 보낸다.
    bot.sendMessage(chat_id=874758964, text='오늘 올라온 Computation and Language의 논문은 '+str(len(results)) +'편입니다.')
    for i in range(len(results)):
        txt_msg = ('Title : ' + results[i]['title'] + '\n' +
              'Authors : ' + results[i]['authors'] + '\n' +
              'Category : ' + results[i]['category'] + '\n'
              'Link : ' + results[i]['link']
              )
        bot.sendMessage(chat_id=874758964, text=txt_msg)


# apscheduler 를 이용하여 매일 아침 8시에 작업 수행
sched = BlockingScheduler()
sched.add_job(job_function, 'cron', hour=8)
sched.start()
