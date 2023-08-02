import sqlite3
import pandas as pd
import argparse
import os


def parse_args():
    desc = "Sqlite2CSV"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--file', '-f', type=str, default='', help='Where is Your Sqlite File?')
    return parser.parse_args()


def main(args):
    full_path = os.path.abspath(args.file)
    file_name = os.path.basename(full_path)
    file_name_without_ext = file_name.split('.')[0]

    conn = sqlite3.connect(full_path)
    query = "SELECT * FROM news"

    clients = pd.read_sql(query, conn)
    clients.to_csv(f'./volume/{file_name_without_ext}.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    args = parse_args()
    if args is None:
        exit()

    main(args)