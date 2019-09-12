# -*- coding: utf-8 -*-

import requests
import telegram
from bs4 import BeautifulSoup


bot = telegram.Bot(token='970060618:AAFbYa2iflYVkwzmoDddsapDXTgJZ0xCKCE')
url = 'https://arxiv.org/list/cs.LG/pastweek?skip=0&show=25'
html = requests.get(url)
bs = BeautifulSoup(html.text, 'html.parser')

info_list = bs.findAll('dd')
link_list = bs.findAll('a', title='Abstract')
link_results = ['https://arxiv.org'+link.attrs['href'] for link in link_list]

results = []

for data, link in zip(info_list, link_results):
    paper_data = {}
    paper_data['title'] = data.find('div', class_='list-title mathjax').text.replace('Title: ','').strip('\n')
    paper_data['authors'] = data.find('div', class_='list-authors').text.replace('Authors:','').replace('\n','')
    paper_data['category'] = data.find('div', class_='list-subjects').text.replace('Subjects: ','').replace('\n','')
    paper_data['link'] = link
    results.append(paper_data)

for i in range(len(results)):
    txt_msg = ('Title : ' + results[i]['title'] + '\n' +
          'Authors : ' + results[i]['authors'] + '\n' +
          'Category : ' + results[i]['category'] + '\n'
          'Link : ' + results[i]['link']
          )
#    print(txt_msg)
    bot.sendMessage(chat_id=874758964, text=txt_msg)
    if i==1:
        break