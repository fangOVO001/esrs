from database import db_session, init_db
from model.Content import Content

import requests
from bs4 import BeautifulSoup

urls = [
  'https://www.dealmoon.co.uk/clothing-jewelry-bags/womens-shoes',
  # 'https://www.dealmoon.co.uk/at-home/luggage-travel-gear'
]

categories = ['shoes', 'luggage']
def spider():
  for idx, url in enumerate(urls):
      print("url: ", url)
      response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
      response.encoding="utf-8"
      soup = BeautifulSoup(response.content, 'html.parser')
      for item in soup.find_all('div', class_='right-cnt'):
          print(item)
          title = item.find('h2', class_='title').text
          content = item.find('p', class_='brief').text
          category = categories[idx]
          from_url = item.find('a', class_='deal-persoanl-strack zoom-title')['href']
          content = Content(title, content, category, from_url)

          db_session.add(content)
          db_session.commit()


