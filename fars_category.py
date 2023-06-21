import sqlite3
import requests
import json

import scripts.database as db

from random import randint
from time import sleep
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup


base_url = 'https://www.farsnews.ir'
db_file_path = './volume/fars_news.db'
db_connection = sqlite3.connect(db_file_path)
db_cursor = db_connection.cursor()

# Import Categories
with open('fars_news_categories.json', encoding="utf-8") as file:
    categories = json.load(file)

try:
    USER_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title CHAR(150),
        short_link CHAR(100),
        service CHAR(50),
        subgroup CHAR(50),
        abstract TEXT,
        body TEXT,
        published_datetime TIMESTAMP
    );'''
    db_cursor.executescript(USER_TABLE_QUERY)
except sqlite3.Error as error:
    print(error)

db_connection.commit()
db_connection.close()

def extract_single_news_information(link, category):
    try:
        page = requests.get(link)
        soup = BeautifulSoup( page.content, 'html.parser' )
        # Get Published Datetime
        published_date_object = soup.select('div.header time')
        if (published_date_object):
            published_date = datetime.strptime(published_date_object[0]['datetime'], '%m/%d/%Y %H:%M:%S %p')
        else:
            published_date = datetime.now().strftime('%m/%d/%Y %H:%M:%S %p')
        
        # Get Title
        title_object = soup.select('h1.title')
        title = title_object[0].get_text().strip()

        # Get Abstract
        abstract_object = soup.select('h1.title + p')
        abstract = abstract_object[0].get_text().strip()

        # Get Service name and Subgroup Name
        service_object = soup.select('div.header h2.category-name a')
        if (len(list(service_object)) == 2):
            service = service_object[0].get_text().strip()
            subgroup = service_object[1].get_text().strip()
        else:
            service = categories[category]
            subgroup = service_object[0].get_text().strip()

        # Get ShortLink
        short_link_object = soup.select('div.short-url')
        short_link = short_link_object[0].get_text().strip()

        #Get Tags
        tags_list_object = soup.select('div.tags a')
        tags_list = []
        for tag in tags_list_object:
            tags_list.append(tag.get_text().strip())

        #Get Body
        body_objects = soup.select('div[itemprop="articleBody"] > p')
        paragraphs = []
        for pr in body_objects:
            paragraphs.append(pr.get_text().strip())
        body = ' '.join(paragraphs)

        
        # Insert into the DB
        db.insert_news_in_database(
            db_file=db_file_path,
            title=title,
            short_link=short_link,
            service=service,
            subgroup=subgroup,
            abstract=abstract,
            body=body,
            published_datetime=published_date,
        )
    except:
        print(link)




def main():
    category = 'university'
    total = 400
    start_from = 0
    for p in tqdm(range(start_from, start_from + total)):
        delay = randint(1,5)
        page = requests.get(f'https://www.farsnews.ir/{category}?p={p}')
        soup = BeautifulSoup( page.content, 'html.parser' )

        news_list = soup.select('div.last-news ul.news-list li > a')
        for link in news_list:
            extract_single_news_information(base_url + link['href'], category)
        sleep(delay)


if __name__ == '__main__':
    main()
