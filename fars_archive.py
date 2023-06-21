import sqlite3
import requests
import json
import sys

import scripts.database as db

from random import randint
from time import sleep
from tqdm import tqdm
from persiantools.jdatetime import JalaliDate
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


base_url = 'https://www.farsnews.ir'
db_file_path = './volume/archive.db'
db_connection = sqlite3.connect(db_file_path)
db_cursor = db_connection.cursor()

# Import Categories
with open('fars_news_categories.json', encoding="utf-8") as file:
    categories = json.load(file)

try:
    USER_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title CHAR(200),
        short_link CHAR(100),
        service CHAR(50),
        subgroup CHAR(50),
        abstract TEXT,
        body TEXT,
        tags CHAR(500),
        published_datetime TIMESTAMP
    );'''
    db_cursor.executescript(USER_TABLE_QUERY)
except sqlite3.Error as error:
    print(error)

db_connection.commit()
db_connection.close()

def extract_single_news_information(link, category):
    try:
        page = requests.get(link, timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')
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
        tags = ', '.join(tags_list)

        #Get Body
        body_objects = soup.select('div[itemprop="articleBody"] > p')
        paragraphs = []
        for pr in body_objects:
            paragraphs.append(pr.get_text().strip())
        body = ' '.join(paragraphs)

        
        # Insert into the DB
        db.insert_news_in_archive(
            db_file=db_file_path,
            title=title,
            short_link=short_link,
            service=service,
            subgroup=subgroup,
            abstract=abstract,
            body=body,
            tags=tags,
            published_datetime=published_date,
        )
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print(link)


def each_day_loop(start_page: int = 0, total_page: int = 50, date: str = ''):
    if date == '':
        return 'You Must Enter The Date'
    else:
        category = 'archive'
        for p in tqdm(range(start_page + 1, start_page + total_page + 1)):
            delay = randint(1,5)
            try:
                page_link = f'https://www.farsnews.ir/archive?cat=-1&subcat=-1&date={date}&p={p}'
                page = requests.get(page_link, timeout=5)
                soup = BeautifulSoup( page.content, 'html.parser' )

                news_list = soup.select('ul.last-news li > a')
                for link in news_list:
                    extract_single_news_information(base_url + link['href'], category)
                sleep(delay)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print(base_url + link['href'])


def main():
    start_date = datetime(2021, 1, 1)
    end_date = datetime.now()
    current_date = start_date
    delay = randint(1,5)
    while current_date <= end_date:
        jalali_date = JalaliDate(current_date)
        formated_date = f'{jalali_date.year}/{jalali_date.month}/{jalali_date.day}'
        each_day_loop(0, 50, formated_date)
        print(f'\n Date {jalali_date.year}-{jalali_date.month}-{jalali_date.day} is finished \n')
        current_date += timedelta(days=1)
        sleep(delay)


if __name__ == '__main__':
    main()