import psycopg2
import db.QUERIES as queries
from db.db_config import config
from db.birthday import Birthday


def __create_connection():
    conn = psycopg2.connect(
        database=config['database'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )
    return conn


def create_tables():
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.create_birthday_table)
    conn.commit()
    cursor.close()
    conn.close()


def drop_tables():
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.delete_birthday_table)
    conn.commit()
    cursor.close()
    conn.close()

# #############


def create_birthday(user_id, day, month, year):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.create_birthday, (user_id, day, month, year))
    conn.commit()
    cursor.close()
    conn.close()


def get_birthday_all():
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.get_birthday_all)
    rows = cursor.fetchall()
    birthdays = []
    for row in rows:
        birthdays.append(Birthday(user_id=row[0], day=row[1], month=row[2], year=row[3]))
    cursor.close()
    conn.close()
    return birthdays


def get_birthday_one(user_id):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.get_birthday_one, (user_id,))
    birthday_data = cursor.fetchone()
    result = None
    if birthday_data:
        result = Birthday(birthday_data[0], birthday_data[1], birthday_data[2], birthday_data[3])
    cursor.close()
    conn.close()
    return result


def update_birthday(user_id, day, month, year):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.update_birthday, (month, day, year, user_id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_birthday(user_id):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.delete_birthday, (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
