import sqlite3


db_file_path = './volume/archive.db'
db_connection = sqlite3.connect(db_file_path)
db_cursor = db_connection.cursor()


# Add deleted_at column to video table
def upgrade():
    db_connection = sqlite3.connect(db_file_path)
    db_cursor = db_connection.cursor()
    query = "ALTER TABLE `news` ADD `agency_name` CHAR(100) DEFAULT 'FarsNews'"
    db_cursor.execute(query)
    db_connection.commit()
    db_connection.close()
    print("NEW COLUMN ADDED..")


# Delete deleted_at column from video table
def downgrade():
    db_connection = sqlite3.connect(db_file_path)
    db_cursor = db_connection.cursor()
    query = "ALTER TABLE `news` DROP `agency_name`;"
    db_cursor.execute(query)
    db_connection.commit()
    db_connection.close()
    print("COLUMN DELETED..")

if __name__ == '__main__':
    upgrade()