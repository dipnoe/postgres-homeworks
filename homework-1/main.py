"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv
import os

KEYS = ('customers', 'employees', 'orders')
PASSWORD: str = os.getenv('PASSWORD')

# поля, не включающие автоинкремент
employees_fields = '("first_name", "last_name", "title", "birth_date", "notes")'


def get_query(key):
    if key == 'customers':
        query = f'INSERT INTO {key} VALUES (%s, %s, %s)'
    elif key == 'employees':
        query = f'INSERT INTO {key} ("first_name", "last_name", "title", "birth_date", "notes")' \
                f'VALUES (%s, %s, %s, %s, %s)'
    else:
        query = f'INSERT INTO {key} VALUES (%s, %s, %s, %s, %s)'
    return query


def get_path(key) -> str:
    file_path = f'north_data/{key}_data.csv'
    return file_path


def csv_reader(csv_file: str):
    """
    Чтение csv файла и получение данных из него
    """
    with open(csv_file, 'r', encoding='utf-8') as file_:
        data = list(csv.reader(file_))
        return data[1:]


def connect_to_db(db_name):
    conn = psycopg2.connect(
        host='localhost',
        database=db_name,
        user='postgres',
        password=PASSWORD
    )
    return conn


def insert_query(file_csv, key):
    """
    Вставка данных из файла в таблицу базы данных
    """
    try:
        with connect_to_db('north') as conn:
            with conn.cursor() as cursor:
                query = get_query(key)
                cursor.executemany(query, file_csv)

    finally:
        conn.close()


if __name__ == '__main__':
    for key_ in KEYS:
        file = csv_reader(get_path(key_))

        if key_ == 'employees':
            insert_query(file, key_)
        else:
            insert_query(file, key_)
