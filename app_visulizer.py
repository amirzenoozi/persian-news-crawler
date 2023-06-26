'''
Check This Link: https://plotly.com/python/
'''
import sqlite3

import pandas as pd
import plotly.express as px

from datetime import datetime
from dash import Dash, html, dash_table, dcc

# Incorporate data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
cnx = sqlite3.connect('./volume/fars_news.db')
df = pd.read_sql_query("SELECT COUNT(*), published_datetime FROM news GROUP BY STRFTIME('%d-%m-%Y', published_datetime) ORDER BY published_datetime ASC;", cnx)

app = Dash(__name__)

chart_data_values = []
chart_data_labels = []
result = df

for index, row in df.iterrows():
    chart_data_values.append(row['COUNT(*)'])
    date_time = datetime.strptime(row['published_datetime'], '%Y-%m-%d %H:%M:%S').strftime("%d %B %Y")
    chart_data_labels.append(date_time)

app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x=chart_data_labels, y=chart_data_values))
])


if __name__ == '__main__':
    app.run_server(debug=True, port=5080)