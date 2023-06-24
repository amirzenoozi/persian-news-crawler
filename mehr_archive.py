import sqlite3
import requests
import json
import sys
import re
import pytz

import scripts.database as db

from random import randint
from time import sleep
from tqdm import tqdm
from persiantools.digits import fa_to_en
from persiantools.characters import ar_to_fa
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from persian import convert_fa_numbers
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

jalali_months = {
    "فروردین": 1,
    "اردیبهشت": 2,
    "خرداد": 3,
    "تیر": 4,
    "مرداد": 5,
    "شهریور": 6,
    "مهر": 7,
    "آبان": 8,
    "آذر": 9,
    "دی": 10,
    "بهمن": 11,
    "اسفند": 12
}


base_url = 'https://www.mehrnews.ir'
db_file_path = './volume/archive.db'
db_connection = sqlite3.connect(db_file_path)
db_cursor = db_connection.cursor()
agency_name = 'MehrNews'

# Import Categories
with open('./statics/mehr_news_categories.json', encoding="utf-8") as file:
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
        published_datetime TIMESTAMP,
        agency_name CHAR(100)
    );'''
    db_cursor.executescript(USER_TABLE_QUERY)
except sqlite3.Error as error:
    print(error)

db_connection.commit()
db_connection.close()

def extract_single_news_information(link, category, agency):
    try:
        page = requests.get(link, timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Get Published Datetime
        published_date_object = soup.select('div.item-header div.item-date')
        if (published_date_object):
            # Convert Persian digits to English digits
            jd_text = published_date_object[0].get_text().strip().split('،')
            jd_time_part = fa_to_en(jd_text[1].strip())
            jd_date_part = fa_to_en(jd_text[0].strip())
            jd_month_name = ar_to_fa(''.join(re.findall(r'\D', jd_date_part))).strip()
            jd_month_number = jalali_months.get(jd_month_name)
            jd_parsed = jd_date_part.replace( jd_month_name, f'-{ jd_month_number }-' ).replace(' ', '').split('-')
            jd_year = int(jd_parsed[2])
            jd_month = int(jd_parsed[1])
            jd_day = int(jd_parsed[0])
            jd_hour = int(jd_time_part.split(':')[0])
            jd_min = int(jd_time_part.split(':')[1])
            gregorian_date = JalaliDateTime(jd_year, jd_month, jd_day, jd_hour, jd_min, 0, 0).to_gregorian()
            published_date = datetime.strftime(gregorian_date, '%m/%d/%Y %H:%M:%S %p')
        else:
            published_date = datetime.now().strftime('%m/%d/%Y %H:%M:%S %p')
        
        # Get Title
        subtitle_object = soup.select('h4.subtitle')
        title_object = soup.select('h1.title')
        subtitle = subtitle_object[0].get_text().strip()
        title = title_object[0].get_text().strip()

        # # Get Abstract
        abstract_object = soup.select('article div.item-summary p')
        try:
            abstract = abstract_object[0].get_text().strip()
        except:
            abstract = 'None'

        # Get Service name and Subgroup Name
        service_object = soup.select('div.item-header ol.breadcrumb a')
        if (len(list(service_object)) == 2):
            service = service_object[0].get_text().strip()
            subgroup = service_object[1].get_text().strip()
        else:
            service = categories[category]
            subgroup = service_object[0].get_text().strip()

        # Get ShortLink
        short_link_object = soup.select('div.short-link-container input')
        try:
            short_link = f'http://{short_link_object[0]["value"].strip()}'
        except:
            short_link = 'None'

        #Get Tags
        tags_list_object = soup.select('section.tags a')
        tags_list = []
        for tag in tags_list_object:
            tags_list.append(tag.get_text().strip())
        tags = ', '.join(tags_list)

        # #Get Body
        body_objects = soup.select('div[itemprop="articleBody"] > p')
        paragraphs = []
        for pr in body_objects:
            paragraphs.append(pr.get_text().strip())
        body = ' '.join(paragraphs)

        
        # Insert into the DB
        db.insert_news_in_archive_multiple_agency(
            db_file=db_file_path,
            title=title,
            short_link=short_link,
            service=service,
            subgroup=subgroup,
            abstract=abstract,
            body=body,
            tags=tags,
            published_datetime=published_date,
            agency_name=agency,
        )
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        # print(link)
        pass


def each_day_loop(start_page: int = 0, total_page: int = 50, year: int = 0, month: int = 0, day: int = 0):
    if year == 0 or month == 0 or day  == 0:
        return 'You Must Enter The Date'
    else:
        category = 'archive'
        tqdm_bar = tqdm(range(start_page + 1, start_page + total_page + 1), desc=f'Page Number #1')
        for p in tqdm_bar:
            delay = randint(1,5)
            try:
                page_link = f'https://www.mehrnews.com/page/archive.xhtml?mn={month}&wide=0&ty=1&dy={day}&ms=0&pi={p}&yr={year}'
                page = requests.get(page_link, timeout=5)
                soup = BeautifulSoup( page.content, 'html.parser' )

                news_list = soup.select('section.list ul > li.news figure > a')
                for link in news_list:
                    extract_single_news_information(base_url + link['href'], category, agency_name)
                tqdm_bar.set_description(f'Page Number #{p}')
                tqdm_bar.refresh()
                sleep(delay)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
                # print(page_link)


def main():
    start_date = datetime(2023, 6, 23)
    end_date = datetime.now()
    current_date = start_date
    delay = randint(1,5)
    while current_date <= end_date:
        jalali_date = JalaliDate(current_date)
        each_day_loop(0, 1, jalali_date.year, jalali_date.month, jalali_date.day)
        print(f'\n==================================')
        print(f'Date {jalali_date.year}-{jalali_date.month}-{jalali_date.day} is finished!')
        print(f'==================================\n')
        current_date += timedelta(days=1)
        sleep(delay)


if __name__ == '__main__':
    main()