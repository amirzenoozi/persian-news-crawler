'''
Check This Link: https://plotly.com/python/
'''

import sqlite3
import json

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

db_file_path = './volume/fars_news.db'
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

def count_single_service_news(service_name):
    db_connection = sqlite3.connect(db_file_path)
    db_cursor = db_connection.cursor()
    query = f"SELECT COUNT(*) FROM news WHERE service = '{service_name}'"
    db_cursor.execute(query)
    result = db_cursor.fetchone()
    db_connection.commit()
    db_connection.close()
    return result[0]


def count_subgroup_in_each_service(service_name):
    db_connection = sqlite3.connect(db_file_path)
    db_cursor = db_connection.cursor()
    query = f"SELECT COUNT(*), subgroup FROM news WHERE service = '{service_name}' GROUP BY subgroup;"
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    db_connection.commit()
    db_connection.close()
    return result




def main():
    chart_data_values = []
    chart_data_labels = []
    for cat in categories:
        count = count_single_service_news(categories[cat])
        chart_data_values.append(count)
        chart_data_labels.append(categories[cat])

    
    # for cat in categories:
        # print(cat)
    sub_count = count_subgroup_in_each_service(categories['social'])
    
    fig = go.Figure(data=[
        go.Bar(x=chart_data_labels, y=chart_data_values, text=chart_data_values, textposition='outside')
    ])
    fig.update_layout(
        title_font_family="IRANSansWeb",
        font_family="IRANSansWeb",
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        xaxis_tickangle=-45,
        hoverlabel=dict(
            font_family="IRANSansWeb"
        ),
    )
    fig.show(config=plt_config)

    
    

if __name__ == '__main__':
    main()