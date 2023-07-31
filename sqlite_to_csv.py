import sqlite3
import pandas as pd


db_file_path = './volume/archive.db'


def main():
    conn = sqlite3.connect(db_file_path)
    query = "SELECT * FROM news"

    clients = pd.read_sql(query, conn)
    clients.to_csv('csv_output.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()