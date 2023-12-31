'''
Check This Link: https://plotly.com/python/
'''

import sqlite3
import json

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from datetime import datetime

db_file_path = './volume/archive.db'
plt_config = {
    'displayModeBar': True,
    'displaylogo': False,
    'autosizable': True,
    'responsive': True,
    'modeBarButtonsToAdd': ['zoom', 'pan'],
    'toImageButtonOptions': {
        'format': 'jpeg',
    }
}

# Import Categories
with open('./statics/fars_news_categories.json', encoding="utf-8") as file:
    categories = json.load(file)


def count_articles_per_month(word):
    db_connection = sqlite3.connect(db_file_path)
    db_cursor = db_connection.cursor()
    query = f"SELECT COUNT(*), published_datetime from news WHERE tags LIKE '%{word}%' GROUP BY STRFTIME('%m-%Y', published_datetime) ORDER BY published_datetime ASC;"
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    db_connection.commit()
    db_connection.close()
    return result



def main():
    chart_data_values = []
    chart_data_labels = []
    result = count_articles_per_month('آمریکا')
    for month in result:
        chart_data_values.append(month[0])
        date_time = datetime.strptime(month[1], '%Y-%m-%d %H:%M:%S')
        chart_data_labels.append(date_time)
    
    fig = go.Figure(data=[
        go.Bar(x=chart_data_labels, y=chart_data_values, text=chart_data_values, textposition='outside')
    ])
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=False
            ),
            type="date"
        ),
        title_font_family="IRANSansWeb",
        font_family="IRANSansWeb",
        uniformtext_minsize=12,
        hoverlabel=dict(
            font_family="IRANSansWeb"
        )
    )
    fig.show(config=plt_config)

    
    

if __name__ == '__main__':
    main()