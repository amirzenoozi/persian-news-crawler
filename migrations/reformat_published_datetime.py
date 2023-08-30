import sqlite3

from datetime import datetime


db_file_path = './volume/archive_v4.db'
db_connection = sqlite3.connect(db_file_path)
db_cursor = db_connection.cursor()

# Add deleted_at column to video table
def upgrade():
    db_connection = sqlite3.connect(db_file_path)
    db_cursor = db_connection.cursor()
    query = "SELECT `id`, `published_datetime` FROM `news` WHERE agency_name = 'FarsNews'"
    db_cursor.execute(query)
    result = db_cursor.fetchall()

    for date in result:
        new_date = datetime.strptime(date[1], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y %H:%M:%S %p')
        update_query = f'UPDATE `news` SET published_datetime = "{new_date}" WHERE id = "{date[0]}"'
        db_cursor.execute(update_query)
    
    db_connection.commit()
    db_connection.close()

if __name__ == '__main__':
    upgrade()