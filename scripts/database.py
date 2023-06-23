"""
Database Scripts
"""
import sqlite3

def insert_news_in_database(db_file, title, short_link, service, subgroup, abstract, body, published_datetime):
    """
    Insert NEWS

    Args:
        db_file (str): Path to Database File
        title (str): News Title

    Returns:
        int: NEWS ID
    """
    db_connection = sqlite3.connect(db_file)
    db_cursor = db_connection.cursor()
    # Check News is Exist Or Not
    find_news_query = """SELECT id FROM news WHERE short_link = (?) LIMIT 1"""
    news = db_cursor.execute(find_news_query, (short_link,)).fetchone()
    # Insert New News
    if not news:
        try:
            add_news_query = """INSERT INTO news (title, short_link, service, subgroup, abstract, body, published_datetime) VALUES (?, ?, ?, ?, ?, ?, ?)"""
            db_cursor.execute(add_news_query, (title, short_link, service, subgroup, abstract, body, published_datetime))
        except sqlite3.Error as error:
            print(error)

    # Close DB Connection
    db_connection.commit()
    db_connection.close()

    return news

def insert_news_in_archive(db_file, title, short_link, service, subgroup, abstract, body, tags, published_datetime):
    """
    Insert NEWS

    Args:
        db_file (str): Path to Database File
        title (str): News Title

    Returns:
        int: NEWS ID
    """
    db_connection = sqlite3.connect(db_file)
    db_cursor = db_connection.cursor()
    # Check News is Exist Or Not
    find_news_query = """SELECT id FROM news WHERE short_link = (?) LIMIT 1"""
    news = db_cursor.execute(find_news_query, (short_link,)).fetchone()
    # Insert New News
    if not news:
        try:
            add_news_query = """INSERT INTO news (title, short_link, service, subgroup, abstract, body, tags, published_datetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            db_cursor.execute(add_news_query, (title, short_link, service, subgroup, abstract, body, tags, published_datetime))
        except sqlite3.Error as error:
            print(error)

    # Close DB Connection
    db_connection.commit()
    db_connection.close()

    return news

def insert_news_in_archive_multiple_agency(db_file, title, short_link, service, subgroup, abstract, body, tags, published_datetime, agency_name):
    """
    Insert NEWS

    Args:
        db_file (str): Path to Database File
        title (str): News Title

    Returns:
        int: NEWS ID
    """
    db_connection = sqlite3.connect(db_file)
    db_cursor = db_connection.cursor()
    # Check News is Exist Or Not
    find_news_query = """SELECT id FROM news WHERE short_link = (?) LIMIT 1"""
    news = db_cursor.execute(find_news_query, (short_link,)).fetchone()
    # Insert New News
    if not news:
        try:
            add_news_query = """INSERT INTO news (title, short_link, service, subgroup, abstract, body, tags, published_datetime, agency_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            db_cursor.execute(add_news_query, (title, short_link, service, subgroup, abstract, body, tags, published_datetime, agency_name))
        except sqlite3.Error as error:
            print(error)

    # Close DB Connection
    db_connection.commit()
    db_connection.close()

    return news