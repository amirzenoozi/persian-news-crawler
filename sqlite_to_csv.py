import sqlite3
import pandas as pd
import argparse
import os


def parse_args():
    desc = "Sqlite2CSV"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', '--file', type=str, default='', help='Where is Your Sqlite File?')
    return parser.parse_args()


def main(args):
    full_path = os.path.abspath(args.file)
    file_name = os.path.basename(full_path)
    file_name_without_ext = file_name.split('.')[0]

    conn = sqlite3.connect(full_path)
    query = "SELECT * FROM news"

    for chunk in pd.read_sql(query, conn, chunksize=500):
        chunk.to_csv(f'./volume/{file_name_without_ext}.csv', mode='a', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    args = parse_args()
    if args is None:
        exit()

    main(args)